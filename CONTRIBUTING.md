# Contributing to LUVORA

Thank you for considering contributing to LUVORA! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots (if applicable)

### Suggesting Features

1. Open an issue with the "enhancement" label
2. Describe the feature and its use case
3. Explain why it would be valuable

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
   ```bash
   python manage.py test
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Describe your changes
   - Reference related issues
   - Wait for review

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small

### Python Formatting

```bash
# Install formatters
pip install black isort flake8

# Format code
black .
isort .

# Check style
flake8 .
```

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for high code coverage

```bash
# Run tests
python manage.py test

# With coverage
coverage run --source='.' manage.py test
coverage report
```

## Documentation

- Update README.md for major changes
- Add docstrings to new functions/classes
- Update QUICKSTART.md if setup process changes

## Commit Messages

Use clear, descriptive commit messages:

- ✅ Good: "Add coupon validation in cart"
- ❌ Bad: "Fix bug"

Format:
```
Type: Brief description

Detailed explanation (if needed)

Related issue: #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/luvora.git
cd luvora

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

## Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged

## Questions?

Feel free to open an issue or reach out to the maintainers.

Thank you for contributing! 🎉
