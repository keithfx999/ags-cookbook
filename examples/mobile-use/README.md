# Mobile Automation: Cloud Sandbox-Based Mobile App Testing

This example demonstrates how to use AgentSandbox cloud sandbox to run Android devices, combined with Appium for mobile app automation tasks.

## Architecture

```
┌─────────────┐     Appium      ┌─────────────┐      ADB       ┌─────────────┐
│   Python    │ ───────────────▶ │   Appium    │ ─────────────▶ │  AgentSandbox  │
│   Script    │                 │   Driver    │                │   (Android) │
└─────────────┘                 └─────────────┘                └─────────────┘
      ▲                                 │                              │
      │                                 │◀─────────────────────────────┘
      │                                 │      Device State / Result
      └─────────────────────────────────┘
              Response
```

**Core Features**:
- Android device runs in cloud sandbox, locally controlled via Appium
- Supports ws-scrcpy for real-time screen streaming
- Complete mobile automation capabilities: app installation, GPS mocking, browser control, Android screen capture, etc.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

You can set configuration in one of three ways:

**Option 1: Environment variables (recommended for CI/CD)**
```bash
export E2B_API_KEY="your_e2b_api_key"
export E2B_DOMAIN="ap-guangzhou.tencentags.com"          # Optional
export SANDBOX_TEMPLATE="mobile-v1"                      # Optional
export SANDBOX_TIMEOUT="3600"                            # Optional (1 hour)
```

**Option 2: .env file (recommended for local development)**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# E2B_API_KEY=your_e2b_api_key
```

**Option 3: Modify the code directly (not recommended)**
Edit the default values in `main.py`.

**Configuration Options:**
- `E2B_API_KEY`: **Required** - Your AgentSandbox API Key
- `E2B_DOMAIN`: Optional, default: `ap-guangzhou.tencentags.com`
- `SANDBOX_TEMPLATE`: Optional, default: `mobile-v1`
- `SANDBOX_TIMEOUT`: Optional, default: `3600` seconds (1 hour)

### 3. Run Example

```bash
python main.py
```

After running, a screen stream URL will be output, allowing you to watch the automation process in real-time.

## Available Features

| Feature | Description |
|---------|-------------|
| `upload_app` | Upload APK to device using chunked upload (supports large files) |
| `install_app` | Install uploaded APK on device |
| `grant_app_permissions` | Grant all necessary permissions to app |
| `launch_app` | Launch installed app |
| `open_browser` | Open URL in device browser |
| `tap_screen` | Tap screen at specified coordinates |
| `take_screenshot` | Take device screenshot |
| `get_location` | Get current GPS location |
| `set_location` | Set GPS location (mock location) |
| `install_and_launch_app` | Complete flow: upload → install → grant permissions → launch |

## Supported Apps

The example includes configurations for common Android apps:

- **WeChat** (`wechat`): Chinese messaging app
- **应用宝** (`yyb`): Chinese app store

You can extend `APP_CONFIGS` dictionary to add more apps.

## Workflow

1. **Create Sandbox**: Start cloud sandbox with Android template
2. **Connect Appium**: Connect to Appium server in sandbox
3. **Device Operations**: Perform various mobile automation tasks
4. **Cleanup**: Close driver and kill sandbox

## Example Usage

### Basic Browser Test

```python
# Open browser and navigate
open_browser(driver, "http://example.com")
time.sleep(5)

# Tap screen
tap_screen(driver, 360, 905)

# Take screenshot
take_screenshot(driver)
```

### App Installation and Launch

```python
# Complete app installation flow
install_and_launch_app(driver, 'yyb')
```

### GPS Location Mocking

```python
# Get current location
get_location(driver)

# Set mock location (Shenzhen, China)
set_location(driver, latitude=22.54347, longitude=113.92972)

# Verify location
get_location(driver)
```

## Chunked Upload

For large APK files, the example uses chunked upload strategy:

1. **Phase 1**: Upload all chunks to temporary directory
2. **Phase 2**: Merge chunks into final APK file

This approach handles large files efficiently and provides progress feedback.

## GPS Location Mocking

The example uses Appium Settings LocationService for GPS mocking, which is suitable for containerized Android environments (redroid). The mock location will be returned when apps request location services.

## Dependencies

- Python >= 3.8
- e2b >= 2.9.0
- Appium-Python-Client >= 3.1.0

## Notes

- **APK files**: Place APK files in the `apk/` directory within this example directory (e.g., `examples/mobile-use/apk/应用宝.apk`). You can also specify a custom path when calling `upload_app()`.
- Screen stream URL uses ws-scrcpy protocol for real-time viewing
- Appium connection uses authentication token from sandbox
- GPS mocking works with LocationService in containerized Android environments
