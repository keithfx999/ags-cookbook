# 贡献指南

感谢您对 Agent Sandbox Cookbook 项目的关注！我们欢迎各种形式的贡献，包括新示例、教程改进、文档优化和 Bug 修复。

## 如何贡献

### 1. 提交 Issue

如果您发现 Bug 或有功能建议，请先搜索现有 Issue，确认没有重复后再创建新 Issue。

创建 Issue 时请包含：
- 清晰的标题和描述
- 复现步骤（如果是 Bug）
- 预期行为和实际行为
- 环境信息（Python 版本、操作系统等）

### 2. 提交 Pull Request

#### 准备工作

1. Fork 本仓库到您的 GitHub 账户
2. 克隆您的 Fork：
   ```bash
   git clone https://github.com/YOUR_USERNAME/ags-cookbook.git
   cd ags-cookbook
   ```
3. 添加上游仓库：
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/ags-cookbook.git
   ```

#### 开发流程

1. 从 `main` 分支创建功能分支：
   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feature/your-feature-name
   ```

2. 进行修改并提交：
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   ```

3. 推送到您的 Fork：
   ```bash
   git push origin feature/your-feature-name
   ```

4. 在 GitHub 上创建 Pull Request

### 3. 代码规范

#### Python 代码规范

- 遵循 [PEP 8](https://pep8.org/) 代码风格
- 使用有意义的变量名和函数名
- 添加必要的注释和文档字符串
- 保持代码简洁易读

#### 提交信息规范

使用语义化提交信息：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

示例：
```
feat: 添加图像处理示例
fix: 修复数据分析示例中的路径问题
docs: 更新 README 安装说明
```

## 示例贡献规范

### 目录结构

新增示例请遵循以下结构：

```
examples/your-example-name/
├── README.md              # 详细说明文档
├── main_script.py         # 主要演示脚本
└── requirements.txt       # 示例专用依赖
```

### README.md 要求

每个示例的 README.md 应包含：

1. **功能描述**：示例实现的功能和使用场景
2. **前置条件**：运行示例所需的环境和配置
3. **安装步骤**：依赖安装命令
4. **运行方法**：完整的执行命令
5. **预期输出**：描述生成的文件和预期结果
6. **代码说明**：关键代码逻辑解释

### 代码要求

- 代码应能独立运行，不依赖其他示例
- 包含完整的错误处理
- 添加必要的日志输出
- 敏感信息（如 API Key）使用环境变量

### requirements.txt 要求

- 指定具体版本号以确保可复现性
- 只包含示例必需的依赖
- 示例：
  ```
  e2b-code-interpreter==1.0.0
  pandas==2.0.0
  ```

## 教程贡献规范

### Jupyter Notebook 规范

- 使用清晰的 Markdown 单元格说明每个步骤
- 代码单元格应能按顺序执行
- 包含预期输出的示例
- 添加必要的注释

### 内容要求

- 从基础概念开始，循序渐进
- 提供完整的代码示例
- 解释关键 API 和参数
- 包含常见问题和解决方案

## 审核流程

1. 提交 PR 后，维护者会进行代码审核
2. 如有修改建议，请及时响应和更新
3. 审核通过后，PR 将被合并到 `main` 分支

## 获取帮助

如果您在贡献过程中遇到问题，可以：

- 在 Issue 中提问
- 查阅项目文档
- 参考现有示例的实现

感谢您的贡献！
