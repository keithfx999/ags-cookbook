# AGS Go SDK Examples

This directory contains usage examples for the AGS (Agent Sandbox) Go SDK.

## Environment Setup

### 1. Set Environment Variables

```bash
export TENCENTCLOUD_SECRET_ID="your-secret-id"
export TENCENTCLOUD_SECRET_KEY="your-secret-key"
```

### 2. Install Dependencies

```bash
go mod tidy
```

## Example List

| Example Function | Description |
|-----------------|-------------|
| `Example_createSandbox` | Create sandbox and get client |
| `Example_runCode_basic` | Run code (basic) |
| `Example_runCode_withContext` | Run code (persistent context) |
| `Example_runCode_onOutput` | Run code (real-time output callback) |
| `Example_filesystem_ops` | File system operations (read/write/list/find/delete/rename/mkdir) |
| `Example_command_run` | Command execution (foreground) |
| `Example_command_background` | Command execution (background + wait) |
| `Example_command_signals` | Command execution (send input and signals) |
| `Example_command_list` | List running processes |
| `Example_core_ops` | Direct use of core list/connect/destroy |

## Running Examples

```bash
go test -v -run Example_createSandbox
go test -v -run Example_runCode_basic
# Or run all examples
go test -v
```

## Core Features

### 1. Create Sandbox

```go
sb, err := sandboxcode.Create(ctx, "code-interpreter-v1", sandboxcode.WithClient(client))
defer func() { _ = sb.Kill(ctx) }()
```

### 2. Run Code

```go
exec, err := sb.Code.RunCode(ctx, "print('hello')", nil, nil)
```

### 3. File Operations

```go
// Write file
sb.Files.Write(ctx, "/home/user/demo.txt", bytes.NewBufferString("hello"), nil)

// Read file
r, err := sb.Files.Read(ctx, "/home/user/demo.txt", nil)
```

### 4. Command Execution

```go
res, err := sb.Commands.Run(ctx, "echo hello", nil, nil)
```

## Dependencies

- `github.com/TencentCloudAgentRuntime/ags-go-sdk` - AGS Go SDK
- `github.com/tencentcloud/tencentcloud-sdk-go` - Tencent Cloud SDK
