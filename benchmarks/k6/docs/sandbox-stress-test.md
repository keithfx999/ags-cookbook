# sandbox-stress-test.js

Full lifecycle stress test script using Tencent Cloud API.

## Description

This script tests the complete sandbox lifecycle: **Create → Get Token → Execute Code → Delete**. It uses Tencent Cloud API with TC3-HMAC-SHA256 signature authentication.

## Required Environment Variables

| Variable | Description |
|----------|-------------|
| `TENCENTCLOUD_SECRET_ID` | Tencent Cloud SecretId |
| `TENCENTCLOUD_SECRET_KEY` | Tencent Cloud SecretKey |

## Optional Environment Variables

### Test Scenario

| Variable | Default | Description |
|----------|---------|-------------|
| `TEST_SCENARIO` | `ramping` | Test scenario: `ramping`, `spike`, `stress`, `soak`, `smoke`, `breakpoint` |

### Ramping Test (default)

| Variable | Default | Description |
|----------|---------|-------------|
| `RAMP_UP_DURATION` | `1m` | Ramp up duration |
| `TARGET_VUS` | `5` | Target virtual users (default for personal quota) |
| `STEADY_DURATION` | `2m` | Steady state duration |
| `RAMP_DOWN_DURATION` | `30s` | Ramp down duration |
| `GRACEFUL_RAMP_DOWN` | `30s` | Graceful ramp down time |

### Spike Test

| Variable | Default | Description |
|----------|---------|-------------|
| `SPIKE_DURATION` | `30s` | Spike duration |
| `SPIKE_VUS` | `10` | Peak virtual users during spike (default for personal quota) |

### Stress Test

| Variable | Default | Description |
|----------|---------|-------------|
| `STRESS_STAGES` | `3` | Number of stress stages |
| `STRESS_STAGE_DURATION` | `1m` | Duration per stage |
| `STRESS_VUS_STEP` | `3` | VUs increment per stage (default for personal quota) |

### Soak Test

| Variable | Default | Description |
|----------|---------|-------------|
| `SOAK_VUS` | `5` | Constant virtual users (default for personal quota) |
| `SOAK_DURATION` | `10m` | Soak test duration |

### Smoke Test

| Variable | Default | Description |
|----------|---------|-------------|
| `SMOKE_VUS` | `1` | Virtual users for smoke test |
| `SMOKE_DURATION` | `1m` | Smoke test duration |

### Thresholds

| Variable | Default | Description |
|----------|---------|-------------|
| `HTTP_REQ_DURATION_P95` | `5000` | HTTP request p95 threshold (ms) |
| `HTTP_REQ_FAILED_RATE` | `0.1` | Max HTTP failure rate |
| `CREATE_DURATION_P95` | `10000` | Create operation p95 threshold (ms) |
| `DELETE_DURATION_P95` | `5000` | Delete operation p95 threshold (ms) |

### Timeout

| Variable | Default | Description |
|----------|---------|-------------|
| `API_TIMEOUT` | `30s` | API request timeout |
| `EXECUTE_TIMEOUT` | `30s` | Code execution timeout |

### Sleep

| Variable | Default | Description |
|----------|---------|-------------|
| `SLEEP_ON_ERROR` | `1` | Sleep duration on error (seconds) |
| `SLEEP_BETWEEN_ITERATIONS` | `1.0` | Sleep between iterations (seconds) |
| `WAIT_AFTER_CREATE` | `0.1` | Wait after create (seconds) |

### Check Thresholds

| Variable | Default | Description |
|----------|---------|-------------|
| `CREATE_TIMEOUT_THRESHOLD` | `15000` | Create timeout check (ms) |
| `EXECUTE_TIMEOUT_THRESHOLD` | `10000` | Execute timeout check (ms) |
| `DELETE_TIMEOUT_THRESHOLD` | `10000` | Delete timeout check (ms) |

### API Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `API_REGION` | `ap-guangzhou` | API region |
| `USE_INTERNAL` | `false` | Use internal network (Tencent Cloud only) |
| `API_HOST` | Auto | API host (auto-selected based on `USE_INTERNAL`) |
| `API_VERSION` | `2025-09-20` | API version |

### Sandbox Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SANDBOX_TOOL_NAME` | `code-interpreter-v1` | Sandbox template name |
| `SANDBOX_PORT` | `49999` | Sandbox port |

### Test Code

| Variable | Default | Description |
|----------|---------|-------------|
| `TEST_CODE` | `print("hello world")` | Code to execute |
| `TEST_LANGUAGE` | `python` | Programming language |

## Usage Examples

```bash
# Basic ramping test (personal quota)
k6 run sandbox-stress-test.js

# Smoke test
k6 run -e TEST_SCENARIO=smoke sandbox-stress-test.js

# Enterprise: Higher VUs after quota increase
k6 run -e TARGET_VUS=100 -e SPIKE_VUS=500 sandbox-stress-test.js

# Use internal network (Tencent Cloud)
k6 run -e USE_INTERNAL=true sandbox-stress-test.js
```

## Quota Notes

Default values are configured for **personal users** (max 10 concurrent sandboxes, 50 QPS API limit).

**Enterprise users** should contact AGS team to request quota increase, then adjust parameters:
```bash
k6 run -e TARGET_VUS=100 -e STRESS_VUS_STEP=50 sandbox-stress-test.js
```
