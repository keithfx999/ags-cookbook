# sandbox-stress-test.js

使用腾讯云 API 的完整生命周期压测脚本。

## 描述

该脚本测试沙箱完整生命周期：**创建 → 获取 Token → 执行代码 → 删除**。使用腾讯云 API，采用 TC3-HMAC-SHA256 签名认证。

## 必需环境变量

| 变量 | 描述 |
|------|------|
| `TENCENTCLOUD_SECRET_ID` | 腾讯云 SecretId |
| `TENCENTCLOUD_SECRET_KEY` | 腾讯云 SecretKey |

## 可选环境变量

### 测试场景

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `TEST_SCENARIO` | `ramping` | 测试场景：`ramping`（渐进）、`spike`（突发）、`stress`（压力）、`soak`（浸泡）、`smoke`（冒烟）、`breakpoint`（断点） |

### 渐进式测试（默认）

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `RAMP_UP_DURATION` | `1m` | 爬升时长 |
| `TARGET_VUS` | `5` | 目标虚拟用户数（个人配额默认值） |
| `STEADY_DURATION` | `2m` | 稳定期时长 |
| `RAMP_DOWN_DURATION` | `30s` | 下降时长 |
| `GRACEFUL_RAMP_DOWN` | `30s` | 优雅下降时间 |

### 突发测试

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `SPIKE_DURATION` | `30s` | 突发持续时长 |
| `SPIKE_VUS` | `10` | 突发峰值虚拟用户数（个人配额默认值） |

### 压力测试

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `STRESS_STAGES` | `3` | 压力阶段数 |
| `STRESS_STAGE_DURATION` | `1m` | 每阶段时长 |
| `STRESS_VUS_STEP` | `3` | 每阶段 VUs 增量（个人配额默认值） |

### 浸泡测试

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `SOAK_VUS` | `5` | 恒定虚拟用户数（个人配额默认值） |
| `SOAK_DURATION` | `10m` | 浸泡测试时长 |

### 冒烟测试

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `SMOKE_VUS` | `1` | 虚拟用户数 |
| `SMOKE_DURATION` | `1m` | 测试时长 |

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
| `EXECUTE_TIMEOUT` | `30s` | 代码执行超时 |

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
| `TEST_CODE` | `print("hello world")` | 执行的代码 |
| `TEST_LANGUAGE` | `python` | 编程语言 |

## 使用示例

```bash
# 基础渐进式测试（个人配额）
k6 run sandbox-stress-test.js

# 冒烟测试
k6 run -e TEST_SCENARIO=smoke sandbox-stress-test.js

# 企业用户：配额提升后使用更高 VUs
k6 run -e TARGET_VUS=100 -e SPIKE_VUS=500 sandbox-stress-test.js

# 使用内网（腾讯云机器）
k6 run -e USE_INTERNAL=true sandbox-stress-test.js
```

## 配额说明

默认值针对**个人用户**配置（最多 10 个并发沙箱，API 限频 50 QPS）。

**企业用户**请联系 AGS 团队申请提升配额，然后调整参数：
```bash
k6 run -e TARGET_VUS=100 -e STRESS_VUS_STEP=50 sandbox-stress-test.js
```
