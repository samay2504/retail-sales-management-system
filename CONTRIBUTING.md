# Contributing to TruEstate

Thank you for your interest in contributing to TruEstate! This document provides guidelines for contributing to the project.

## Code of Conduct

Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in GitHub Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, Python/Node version, etc.)

### Suggesting Features

1. Check if the feature has been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes following the code standards
4. Add tests for new functionality
5. Ensure all tests pass: `make test`
6. Run linters: `make lint`
7. Commit with clear messages
8. Push to your fork
9. Create a Pull Request with:
   - Description of changes
   - Related issue numbers
   - Screenshots for UI changes

## Code Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use Black for formatting (line length: 100)
- Use Ruff for linting
- Type hints required for all functions
- Docstrings for public APIs
- Tests required (pytest)

```bash
# Format code
black src tests

# Lint code
ruff check src tests

# Run tests
pytest --cov=src
```

### TypeScript (Frontend)

- Follow ESLint rules
- Use Prettier for formatting
- Strict TypeScript mode
- Functional components with hooks
- Tests required (Vitest)

```bash
# Format code
npm run format

# Lint code
npm run lint

# Run tests
npm run test
```

## Commit Messages

Use conventional commit format:

```
type(scope): subject

body

footer
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

Example:
```
feat(api): add customer export endpoint

Add new endpoint to export customer data as CSV.
Includes pagination and filtering support.

Closes #123
```

## Development Setup

See README.md for detailed setup instructions.

Quick start:
```bash
# Setup
make setup
make install

# Development
make dev-backend  # Terminal 1
make dev-frontend # Terminal 2

# Testing
make test

# Linting
make lint
```

## Questions?

Open a GitHub Discussion or Issue for questions about contributing.

Thank you for contributing! 🎉
