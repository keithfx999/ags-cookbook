# AGS Go SDK 示例

本目录包含 AGS (Agent Sandbox) Go SDK 的使用示例。

## 环境准备

### 1. 设置环境变量

```bash
export TENCENTCLOUD_SECRET_ID="your-secret-id"
export TENCENTCLOUD_SECRET_KEY="your-secret-key"
```

### 2. 安装依赖

```bash
go mod tidy
```

## 示例列表

| 示例函数 | 说明 |
|---------|------|
| `Example_createSandbox` | 创建沙箱并获取客户端 |
| `Example_runCode_basic` | 运行代码（基础） |
| `Example_runCode_withContext` | 运行代码（持久化上下文） |
| `Example_runCode_onOutput` | 运行代码（实时输出回调） |
| `Example_filesystem_ops` | 文件系统操作（读/写/列/查/删/改名/建目录） |
| `Example_command_run` | 命令执行（前台运行） |
| `Example_command_background` | 命令执行（后台运行 + 等待） |
| `Example_command_signals` | 命令执行（发送输入与信号） |
| `Example_command_list` | 列出运行中进程 |
| `Example_core_ops` | 直接使用 core 列表/连接/销毁 |

## 运行示例

```bash
go test -v -run Example_createSandbox
go test -v -run Example_runCode_basic
# 或运行所有示例
go test -v
```

## 核心功能

### 1. 创建沙箱

```go
sb, err := sandboxcode.Create(ctx, "code-interpreter-v1", sandboxcode.WithClient(client))
defer func() { _ = sb.Kill(ctx) }()
```

### 2. 运行代码

```go
exec, err := sb.Code.RunCode(ctx, "print('hello')", nil, nil)
```

### 3. 文件操作

```go
// 写文件
sb.Files.Write(ctx, "/home/user/demo.txt", bytes.NewBufferString("hello"), nil)

// 读文件
r, err := sb.Files.Read(ctx, "/home/user/demo.txt", nil)
```

### 4. 命令执行

```go
res, err := sb.Commands.Run(ctx, "echo hello", nil, nil)
```

## 依赖

- `github.com/TencentCloudAgentRuntime/ags-go-sdk` - AGS Go SDK
- `github.com/tencentcloud/tencentcloud-sdk-go` - 腾讯云 SDK
