import 'dotenv/config';
import { Sandbox } from '@e2b/code-interpreter';
import http from 'http';
import httpProxy from 'http-proxy';

// 本地代理服务器端口
const LOCAL_PROXY_PORT = 3000;
// OpenClaw 在沙箱内通过 nginx 反向代理暴露的端口（nginx 8080 → openclaw 18789）
const OPENCLAW_PORT = 8080;

// ---------------------------------------------------------------------------
// 本地代理
// ---------------------------------------------------------------------------

function createLocalProxy(targetHost: string, accessToken: string, instanceId: string) {
  const proxy = httpProxy.createProxyServer({
    target: `https://${targetHost}`,
    changeOrigin: true,
    secure: true,
    ws: true,
  });

  proxy.on('proxyReq', (proxyReq, req) => {
    proxyReq.setHeader('X-Access-Token', accessToken);
    console.log('Proxying:', req.url);
  });

  proxy.on('proxyReqWs', (proxyReq, req) => {
    proxyReq.setHeader('X-Access-Token', accessToken);
  });

  proxy.on('error', (err, _req, res) => {
    console.error('Proxy error:', err.message);
    if (res && 'writeHead' in res) {
      (res as http.ServerResponse).writeHead(502);
      (res as http.ServerResponse).end('Bad Gateway: ' + err.message);
    }
  });

  // Strip /{instanceId} prefix before forwarding to OpenClaw
  const prefix = `/${instanceId}`;
  function rewriteUrl(url: string): string {
    if (url === prefix || url.startsWith(prefix + '/') || url.startsWith(prefix + '?')) {
      return url.slice(prefix.length) || '/';
    }
    return url;
  }

  const server = http.createServer((req, res) => {
    req.url = rewriteUrl(req.url || '/');
    proxy.web(req, res);
  });

  server.on('upgrade', (req, socket, head) => {
    socket.on('error', (err) => {
      console.error('WebSocket socket error:', err.message);
    });
    req.url = rewriteUrl(req.url || '/');
    proxy.ws(req, socket, head);
  });

  return server;
}

function startProxy(remoteHost: string, accessToken: string, instanceId: string): http.Server {
  const server = createLocalProxy(remoteHost, accessToken, instanceId);
  server.listen(LOCAL_PROXY_PORT, () => {
    console.log(`✅ 本地代理服务器已启动`);
    console.log(`\n🌐 OpenClaw Dashboard: http://localhost:${LOCAL_PROXY_PORT}/${instanceId}/`);
    console.log('💡 按 Ctrl+C 退出');
  });
  return server;
}

// ---------------------------------------------------------------------------
// 健康探针
// ---------------------------------------------------------------------------

async function waitForOpenClaw(sbx: Sandbox, port: number, timeoutMs = 120000): Promise<void> {
  console.log(`\n⏳ 等待 OpenClaw 在端口 ${port} 就绪（最多 ${timeoutMs / 1000}s）...`);
  const deadline = Date.now() + timeoutMs;
  let attempt = 0;

  while (Date.now() < deadline) {
    attempt++;
    try {
      const result = await sbx.commands.run(
        `curl -sf http://localhost:${port}/ -o /dev/null -w "%{http_code}" --max-time 3 2>/dev/null; echo`
      );
      const output = result.stdout?.trim();
      if (output && /^2\d\d$/.test(output)) {
        console.log(`✅ OpenClaw 已就绪（HTTP ${output}），共等待 ${attempt} 次探针`);
        return;
      }
    } catch {
      // 忽略，继续重试
    }
    process.stdout.write(`\r  探针 #${attempt}...`);
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  console.warn('\n⚠️  OpenClaw 启动超时，但仍继续启动代理（OpenClaw 可能还需要更多时间）');
}

// ---------------------------------------------------------------------------
// 退出处理
// ---------------------------------------------------------------------------

function onExit(server: http.Server, killSandbox: () => Promise<void>) {
  let isCleaningUp = false;
  const cleanup = async () => {
    if (isCleaningUp) return;
    isCleaningUp = true;
    console.log('\n\n🛑 正在关闭...');
    // closeAllConnections 强制断开所有 keep-alive/WebSocket 连接，避免 close() 挂住
    server.closeAllConnections();
    console.log('✅ 本地代理服务器已关闭');
    await killSandbox();
    process.exit(0);
  };
  process.on('SIGINT', cleanup);
  process.on('SIGTERM', cleanup);
}

// ---------------------------------------------------------------------------
// start：创建新沙箱，退出时销毁
// ---------------------------------------------------------------------------

async function cmdStart() {
  console.log('🚀 启动 OpenClaw 沙箱...\n');

  const sbx = await Sandbox.create(process.env.TEMPLATE || '', {
    timeoutMs: 30 * 60 * 1000,
  });
  console.log('✅ 沙箱创建成功，ID:', sbx.sandboxId);

  await waitForOpenClaw(sbx, OPENCLAW_PORT);

  const remoteHost = sbx.getHost(OPENCLAW_PORT);
  const accessToken = (sbx as any).envdAccessToken as string;

  console.log('\n📝 启动本地代理服务器...');
  const server = startProxy(remoteHost, accessToken, sbx.sandboxId);
  console.log('   （Ctrl+C 将同时关闭代理并销毁沙箱）');

  onExit(server, async () => {
    await sbx.kill();
    console.log('✅ 沙箱已销毁');
  });

  await new Promise(() => {});
}

// ---------------------------------------------------------------------------
// connect：连接到已有沙箱，退出时仅停止代理
// ---------------------------------------------------------------------------

async function cmdConnect(sandboxId: string) {
  console.log(`🔌 连接到沙箱 ${sandboxId}...\n`);

  const sbx = await Sandbox.connect(sandboxId);
  console.log('✅ 已连接，沙箱 ID:', sbx.sandboxId);

  const remoteHost = sbx.getHost(OPENCLAW_PORT);
  const accessToken = (sbx as any).envdAccessToken as string;

  console.log('\n📝 启动本地代理服务器...');
  const server = startProxy(remoteHost, accessToken, sbx.sandboxId);
  console.log('   （Ctrl+C 将仅停止代理，沙箱保持运行）');

  onExit(server, async () => {
    // connect 模式不销毁沙箱
    console.log(`💡 沙箱 ${sbx.sandboxId} 仍在运行，可用以下命令重新连接：`);
    console.log(`   pnpm start connect ${sbx.sandboxId}`);
  });

  await new Promise(() => {});
}

// ---------------------------------------------------------------------------
// 入口
// ---------------------------------------------------------------------------

const [, , command, arg] = process.argv;

if (command === 'connect') {
  if (!arg) {
    console.error('用法: pnpm connect <sandbox_id>');
    process.exit(1);
  }
  cmdConnect(arg).catch(console.error);
} else {
  // 默认走 start（兼容旧的 pnpm start）
  cmdStart().catch(console.error);
}
