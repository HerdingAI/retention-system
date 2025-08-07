# Contributing to Student Retention Prediction System

We welcome contributions to improve the Student Retention Prediction System! This document provides guidelines for contributing to the project.

## How to Contribute

### 1. Fork the Repository
Fork the project on GitHub and clone your fork locally.

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes
- Write clean, documented code
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed

### 4. Test Your Changes
```bash
# Run the test suite
python tests/system_test.py

# Test manually with the web interface
python simple_api.py
# Open examples/api_test.html in browser
```

### 5. Submit a Pull Request
- Write a clear commit message
- Describe your changes in the PR description
- Reference any related issues

## Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/student-retention-prediction.git
cd student-retention-prediction
```

2. **Create virtual environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the API**
```bash
python simple_api.py
```

## Code Style Guidelines

- Use clear, descriptive variable names
- Add docstrings to functions and classes
- Follow PEP 8 style guidelines
- Keep functions focused and small
- Add type hints where appropriate

## Testing Guidelines

- Write tests for new features
- Ensure all tests pass before submitting
- Test both success and error cases
- Update test documentation

## Documentation

- Update README.md for significant changes
- Add inline comments for complex logic
- Update API documentation for endpoint changes
- Include examples for new features

## Reporting Issues

When reporting issues:
- Use a clear, descriptive title
- Provide steps to reproduce the issue
- Include system information (OS, Python version)
- Add relevant error messages or logs

## Feature Requests

For feature requests:
- Describe the problem you're trying to solve
- Explain your proposed solution
- Consider alternative approaches
- Discuss potential impact on existing features

## Questions?

Feel free to open an issue for questions about:
- How to implement a feature
- Architecture decisions
- Best practices
- Getting started with development

Thank you for contributing to help educational institutions improve student success!
