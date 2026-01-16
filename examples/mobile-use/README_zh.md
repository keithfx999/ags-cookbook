# Mobile Automation: 基于云端沙箱的移动端自动化测试

本示例展示如何使用 AgentSandbox 云端沙箱运行 Android 设备，结合 Appium 实现移动端应用自动化任务。

## 架构

```
┌─────────────┐     Appium      ┌─────────────┐      ADB       ┌─────────────┐
│   Python    │ ───────────────▶ │   Appium    │ ─────────────▶ │  AgentSandbox  │
│   脚本      │                 │   Driver    │                │   (Android) │
└─────────────┘                 └─────────────┘                └─────────────┘
      ▲                                 │                              │
      │                                 │◀─────────────────────────────┘
      │                                 │      设备状态 / 结果
      └─────────────────────────────────┘
              响应
```

**核心特性**：
- Android 设备运行在云端沙箱，本地通过 Appium 远程控制
- 支持 ws-scrcpy 实时屏幕流查看
- 完整的移动端自动化能力：应用安装、GPS 模拟、浏览器控制、安卓界面截图等

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

可以通过以下三种方式之一进行配置：

**方式1：环境变量（推荐用于 CI/CD）**
```bash
export E2B_API_KEY="your_e2b_api_key"
export E2B_DOMAIN="ap-guangzhou.tencentags.com"          # 可选
export SANDBOX_TEMPLATE="mobile-v1"                      # 可选
export SANDBOX_TIMEOUT="3600"                            # 可选 (1小时)
```

**方式2：.env 文件（推荐用于本地开发）**
```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 并添加你的 API key
# E2B_API_KEY=your_e2b_api_key
```

**方式3：直接修改代码（不推荐）**
编辑 `main.py` 中的默认值。

**配置选项：**
- `E2B_API_KEY`: **必需** - 你的 AgentSandbox API Key
- `E2B_DOMAIN`: 可选，默认: `ap-guangzhou.tencentags.com`
- `SANDBOX_TEMPLATE`: 可选，默认: `mobile-v1`
- `SANDBOX_TIMEOUT`: 可选，默认: `3600` 秒（1小时）

### 3. 运行示例

```bash
python main.py
```

运行后会输出屏幕流地址，可在浏览器中实时观看自动化过程。

## 可用功能

| 功能 | 说明 |
|------|------|
| `upload_app` | 使用分片上传将 APK 上传到设备（支持大文件） |
| `install_app` | 在设备上安装已上传的 APK |
| `grant_app_permissions` | 授予应用所有必要权限 |
| `launch_app` | 启动已安装的应用 |
| `open_browser` | 在设备浏览器中打开 URL |
| `tap_screen` | 点击屏幕指定坐标 |
| `take_screenshot` | 截取设备屏幕截图 |
| `get_location` | 获取当前 GPS 定位 |
| `set_location` | 设置 GPS 定位（模拟位置） |
| `install_and_launch_app` | 完整流程：上传 → 安装 → 授权 → 启动 |

## 支持的应用

示例包含常见 Android 应用的配置：

- **微信** (`wechat`): 中文即时通讯应用
- **应用宝** (`yyb`): 中文应用商店

可以通过扩展 `APP_CONFIGS` 字典来添加更多应用。

## 工作流程

1. **创建沙箱**：启动 Android 模板的云端沙箱
2. **连接 Appium**：连接到沙箱内的 Appium 服务
3. **设备操作**：执行各种移动端自动化任务
4. **清理资源**：关闭驱动并销毁沙箱

## 使用示例

### 基础浏览器测试

```python
# 打开浏览器并导航
open_browser(driver, "http://example.com")
time.sleep(5)

# 点击屏幕
tap_screen(driver, 360, 905)

# 截图
take_screenshot(driver)
```

### 应用安装和启动

```python
# 完整的应用安装流程
install_and_launch_app(driver, 'yyb')
```

### GPS 定位模拟

```python
# 获取当前位置
get_location(driver)

# 设置模拟位置（深圳）
set_location(driver, latitude=22.54347, longitude=113.92972)

# 验证位置
get_location(driver)
```

## 分片上传

对于大型 APK 文件，示例使用分片上传策略：

1. **阶段1**：将所有分片上传到临时目录
2. **阶段2**：将分片合并为最终的 APK 文件

这种方式可以高效处理大文件，并提供进度反馈。

## GPS 定位模拟

示例使用 Appium Settings LocationService 进行 GPS 模拟，适用于容器化 Android 环境（redroid）。当应用请求位置服务时，将返回模拟位置。

## 依赖

- Python >= 3.8
- e2b >= 2.9.0
- Appium-Python-Client >= 3.1.0

## 注意事项

- **APK 文件**：将 APK 文件放在本示例目录下的 `apk/` 目录中（例如：`examples/mobile-use/apk/应用宝.apk`）。也可以在调用 `upload_app()` 时指定自定义路径。
- 屏幕流地址使用 ws-scrcpy 协议进行实时查看
- Appium 连接使用沙箱的认证令牌
- GPS 模拟在容器化 Android 环境中通过 LocationService 工作
