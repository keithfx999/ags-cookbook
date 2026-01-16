# Contributing Guide

Thank you for your interest in the Agent Sandbox Cookbook project! We welcome all forms of contributions, including new examples, tutorial improvements, documentation enhancements, and bug fixes.

## How to Contribute

### 1. Submit an Issue

If you find a bug or have a feature suggestion, please search existing issues first to ensure there are no duplicates before creating a new issue.

When creating an issue, please include:
- A clear title and description
- Steps to reproduce (if it's a bug)
- Expected behavior and actual behavior
- Environment information (Python version, operating system, etc.)

### 2. Submit a Pull Request

#### Preparation

1. Fork this repository to your GitHub account
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ags-cookbook.git
   cd ags-cookbook
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/ags-cookbook.git
   ```

#### Development Workflow

1. Create a feature branch from `main`:
   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feature/your-feature-name
   ```

2. Make changes and commit:
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request on GitHub

### 3. Code Standards

#### Python Code Standards

- Follow [PEP 8](https://pep8.org/) code style
- Use meaningful variable and function names
- Add necessary comments and docstrings
- Keep code clean and readable

#### Commit Message Standards

Use semantic commit messages:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `style:` Code formatting changes
- `refactor:` Code refactoring
- `test:` Test-related
- `chore:` Build/tool-related

Examples:
```
feat: add image processing example
fix: fix path issue in data analysis example
docs: update README installation instructions
```

## Example Contribution Guidelines

### Directory Structure

New examples should follow this structure:

```
examples/your-example-name/
├── README.md              # Detailed documentation
├── main_script.py         # Main demo script
└── requirements.txt       # Example-specific dependencies
```

### README.md Requirements

Each example's README.md should include:

1. **Feature Description**: Functionality and use cases of the example
2. **Prerequisites**: Required environment and configuration
3. **Installation Steps**: Dependency installation commands
4. **Running Instructions**: Complete execution commands
5. **Expected Output**: Description of generated files and expected results
6. **Code Explanation**: Key code logic explanation

### Code Requirements

- Code should run independently without depending on other examples
- Include complete error handling
- Add necessary logging output
- Use environment variables for sensitive information (e.g., API Keys)

### requirements.txt Requirements

- Specify exact version numbers to ensure reproducibility
- Only include dependencies required by the example
- Example:
  ```
  e2b-code-interpreter==1.0.0
  pandas==2.0.0
  ```

## Tutorial Contribution Guidelines

### Jupyter Notebook Standards

- Use clear Markdown cells to explain each step
- Code cells should be executable in sequence
- Include examples of expected output
- Add necessary comments

### Content Requirements

- Start with basic concepts and progress gradually
- Provide complete code examples
- Explain key APIs and parameters
- Include common questions and solutions

## Review Process

1. After submitting a PR, maintainers will conduct a code review
2. If there are suggestions for changes, please respond and update promptly
3. Once approved, the PR will be merged into the `main` branch

## Getting Help

If you encounter problems during the contribution process, you can:

- Ask questions in Issues
- Refer to project documentation
- Reference existing example implementations

Thank you for your contribution!
