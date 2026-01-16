# sandbox-stress-test-data-plane.js

用于长时间代码执行的数据平面压测脚本。

## 描述

该脚本专为数据平面压力测试设计，执行长时间运行的代码。它创建沙箱，执行可配置时长（默认 30 秒）的代码，并维持高并发连接。使用腾讯云 API，采用 TC3-HMAC-SHA256 签名认证。

## 使用场景

- 测试高并发长连接下的数据平面容量
- 测量系统在持续 WebSocket/HTTP 连接下的行为
- 寻找最大并发沙箱执行上限

## 必需环境变量

| 变量 | 描述 |
|------|------|
| `TENCENTCLOUD_SECRET_ID` | 腾讯云 SecretId |
| `TENCENTCLOUD_SECRET_KEY` | 腾讯云 SecretKey |

## 可选环境变量

### 数据平面压测配置

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `MAX_VUS` | `5` | 最大虚拟用户数（个人配额默认值） |
| `VUS_INCREASE_PER_SECOND` | `1` | 每秒 VUs 增长速率（个人配额慢速爬升） |
| `CODE_EXECUTION_DURATION` | `30` | 代码执行时长（秒） |
| `STEADY_DURATION` | `2m` | 维持最大 VUs 的时长 |
| `RAMP_DOWN_DURATION` | `30s` | 下降时长 |
| `GRACEFUL_RAMP_DOWN` | `30s` | 优雅下降时间 |

### 阈值配置

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `HTTP_REQ_DURATION_P95` | `5000` | HTTP 请求 p95 阈值（毫秒） |
| `HTTP_REQ_FAILED_RATE` | `0.1` | 最大 HTTP 失败率 |
| `CREATE_DURATION_P95` | `10000` | 创建操作 p95 阈值（毫秒） |
| `DELETE_DURATION_P95` | `5000` | 删除操作 p95 阈值（毫秒） |

### 超时配置

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `API_TIMEOUT` | `30s` | API 请求超时 |
| `EXECUTE_TIMEOUT` | `3m` | 代码执行超时（数据平面测试需要更长时间） |

### 休眠配置

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `SLEEP_ON_ERROR` | `1` | 错误后休眠时长（秒） |
| `SLEEP_BETWEEN_ITERATIONS` | `1.0` | 迭代间休眠时长（秒） |
| `WAIT_AFTER_CREATE` | `0.1` | 创建后等待时长（秒） |

### 检查阈值

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `CREATE_TIMEOUT_THRESHOLD` | `15000` | 创建超时检查（毫秒） |
| `EXECUTE_TIMEOUT_THRESHOLD` | `10000` | 执行超时检查（毫秒） |
| `DELETE_TIMEOUT_THRESHOLD` | `10000` | 删除超时检查（毫秒） |

### API 配置

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `API_REGION` | `ap-guangzhou` | API 区域 |
| `USE_INTERNAL` | `false` | 使用内网（仅限腾讯云机器） |
| `API_HOST` | 自动 | API 主机（根据 `USE_INTERNAL` 自动选择） |
| `API_VERSION` | `2025-09-20` | API 版本 |

### 沙箱配置

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `SANDBOX_TOOL_NAME` | `code-interpreter-v1` | 沙箱模板名称 |
| `SANDBOX_PORT` | `49999` | 沙箱端口 |

### 测试代码

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `TEST_CODE` | `import time\ntime.sleep(30)` | 执行的代码（默认休眠 CODE_EXECUTION_DURATION 秒） |
| `TEST_LANGUAGE` | `python` | 编程语言 |

## 使用示例

```bash
# 默认数据平面压测（个人配额：5 VUs，30 秒执行）
k6 run sandbox-stress-test-data-plane.js

# 自定义最大 VUs 和执行时长
k6 run -e MAX_VUS=8 -e CODE_EXECUTION_DURATION=60 sandbox-stress-test-data-plane.js

# 企业用户：配额提升后使用更高 VUs
k6 run -e MAX_VUS=2000 -e VUS_INCREASE_PER_SECOND=100 sandbox-stress-test-data-plane.js

# 使用内网
k6 run -e USE_INTERNAL=true sandbox-stress-test-data-plane.js
```

## 注意事项

- 爬升时长自动计算：`MAX_VUS / VUS_INCREASE_PER_SECOND`
- 每个 VU 在代码执行期间维持一个长连接
- 默认值针对**个人配额**配置（最多 10 个并发沙箱）
- **企业用户**：联系 AGS 团队申请配额提升后再运行高 VU 测试
