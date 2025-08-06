# Contributing to TaskbarManager

Thank you for your interest in contributing to TaskbarManager! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Windows operating system (required for Windows API functionality)
- Git for version control

### Development Setup

1. **Fork and Clone the Repository**

   ```bash
   git clone https://github.com/AltafEmpaxis/InterviewReady.git
   cd InterviewReady
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]  # Install development dependencies
   ```

4. **Run the Application**
   ```bash
   python src/taskbar_manager.py
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep line length under 88 characters (Black formatter standard)

### Testing

- Run the application manually to test changes
- Test on different Windows versions if possible
- Verify that all features work as expected

### Git Workflow

1. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**

   - Keep commits focused and atomic
   - Write clear commit messages
   - Test your changes thoroughly

3. **Submit a Pull Request**
   - Push your branch to GitHub
   - Create a pull request with a clear description
   - Link any related issues

### Commit Message Format

Use clear, descriptive commit messages:

```
Add: New feature description
Fix: Bug fix description
Update: Improvement description
Remove: Removal description
```

## Types of Contributions

### Bug Reports

When reporting bugs, please include:

- Windows version
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

### Feature Requests

For new features, please:

- Describe the feature clearly
- Explain the use case
- Consider backwards compatibility
- Discuss implementation approach

### Code Contributions

We welcome contributions for:

- Bug fixes
- New features
- Performance improvements
- UI/UX enhancements
- Documentation improvements
- Code refactoring

## Windows API Considerations

This application uses Windows APIs through pywin32. When contributing:

- Understand the Windows API functions being used
- Handle errors gracefully
- Test with different window types and applications
- Consider security implications
- Document any new API usage

## Security Guidelines

- Never execute arbitrary code from external sources
- Validate all user inputs
- Handle permissions and admin requirements safely
- Be cautious with process manipulation functions

## Pull Request Process

1. **Before Submitting**

   - Test your changes thoroughly
   - Update documentation if needed
   - Add comments for complex logic
   - Ensure code follows style guidelines

2. **Pull Request Description**

   - Clearly describe what changes were made
   - Reference any related issues
   - Include screenshots for UI changes
   - List any breaking changes

3. **Review Process**
   - Maintainers will review your PR
   - Address any feedback or requested changes
   - Keep the PR up to date with the main branch

## Questions and Support

If you have questions about contributing:

- Check existing issues and discussions
- Create a new issue for questions
- Be respectful and professional in all interactions

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to TaskbarManager!
