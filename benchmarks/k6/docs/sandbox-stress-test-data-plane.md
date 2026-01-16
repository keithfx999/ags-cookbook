# sandbox-stress-test-data-plane.js

Data plane stress test script for long-running code execution.

## Description

This script is designed for data plane stress testing with long-running code execution. It creates sandboxes, executes code that runs for a configurable duration (default 30 seconds), and maintains high concurrent connections. Uses Tencent Cloud API with TC3-HMAC-SHA256 signature authentication.

## Use Case

- Test data plane capacity under high concurrent long-running connections
- Measure system behavior with sustained WebSocket/HTTP connections
- Find maximum concurrent sandbox execution limits

## Required Environment Variables

| Variable | Description |
|----------|-------------|
| `TENCENTCLOUD_SECRET_ID` | Tencent Cloud SecretId |
| `TENCENTCLOUD_SECRET_KEY` | Tencent Cloud SecretKey |

## Optional Environment Variables

### Data Plane Stress Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_VUS` | `5` | Maximum virtual users (default for personal quota) |
| `VUS_INCREASE_PER_SECOND` | `1` | VUs increase rate per second (slow ramp for personal quota) |
| `CODE_EXECUTION_DURATION` | `30` | Code execution duration (seconds) |
| `STEADY_DURATION` | `2m` | Keep max VUs for this duration |
| `RAMP_DOWN_DURATION` | `30s` | Ramp down duration |
| `GRACEFUL_RAMP_DOWN` | `30s` | Graceful ramp down time |

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
| `EXECUTE_TIMEOUT` | `3m` | Code execution timeout (longer for data plane) |

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
| `TEST_CODE` | `import time\ntime.sleep(30)` | Code to execute (default sleeps for CODE_EXECUTION_DURATION) |
| `TEST_LANGUAGE` | `python` | Programming language |

## Usage Examples

```bash
# Default data plane stress test (personal quota: 5 VUs, 30s execution)
k6 run sandbox-stress-test-data-plane.js

# Custom max VUs and execution duration
k6 run -e MAX_VUS=8 -e CODE_EXECUTION_DURATION=60 sandbox-stress-test-data-plane.js

# Enterprise: Higher VUs after quota increase
k6 run -e MAX_VUS=2000 -e VUS_INCREASE_PER_SECOND=100 sandbox-stress-test-data-plane.js

# Use internal network
k6 run -e USE_INTERNAL=true sandbox-stress-test-data-plane.js
```

## Notes

- The ramp-up duration is automatically calculated: `MAX_VUS / VUS_INCREASE_PER_SECOND`
- Each VU maintains a long-running connection during code execution
- Default values are for **personal quota** (max 10 concurrent sandboxes)
- **Enterprise users**: Contact AGS team to request quota increase for high-VU tests
