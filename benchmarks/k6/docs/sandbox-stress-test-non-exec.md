# sandbox-stress-test-non-exec.js

Control plane stress test script (Create/Delete only, no code execution).

## Description

This script tests the control plane operations only: **Create → Delete**. It skips token acquisition and code execution, focusing purely on sandbox lifecycle management. Uses Tencent Cloud API with TC3-HMAC-SHA256 signature authentication.

## Use Case

- Test control plane capacity without data plane overhead
- Measure pure create/delete throughput
- Isolate control plane performance from execution performance

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
| `RAMP_UP_DURATION` | `30s` | Ramp up duration |
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
| `EXECUTE_TIMEOUT` | `30s` | Code execution timeout (not used in this script) |

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

## Usage Examples

```bash
# Basic control plane test (personal quota)
k6 run sandbox-stress-test-non-exec.js

# Smoke test
k6 run -e TEST_SCENARIO=smoke sandbox-stress-test-non-exec.js

# Enterprise: Higher VUs after quota increase
k6 run -e TARGET_VUS=200 -e SLEEP_BETWEEN_ITERATIONS=0.5 sandbox-stress-test-non-exec.js

# Use internal network
k6 run -e USE_INTERNAL=true sandbox-stress-test-non-exec.js
```

## Notes

- This script does NOT execute any code in the sandbox
- Useful for isolating control plane performance
- Each iteration makes 2 API calls: StartSandboxInstance + StopSandboxInstance
- Default values are for **personal quota** (max 10 concurrent sandboxes)
- **Enterprise users**: Contact AGS team to request quota increase
