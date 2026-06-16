# Testing Guide - Form Studio

This document provides comprehensive instructions for testing the Form Studio project, including both backend (Python/FastAPI) and frontend (React) components.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Backend Testing](#backend-testing)
- [Frontend Testing](#frontend-testing)
- [Running All Tests](#running-all-tests)
- [Test Coverage](#test-coverage)
- [CI/CD Integration](#cicd-integration)

## 🚀 Quick Start

### Prerequisites
Ensure your environment is set up:
```bash
# Install all dependencies
npm run install:all

# Or manually:
npm install
pip install -r requirements.txt
```

### Run All Tests
```bash
npm run test:all
```

## 🧪 Backend Testing

The backend uses **pytest** for unit and integration testing.

### Setup
```bash
# Install test dependencies (included in requirements.txt)
pip install -r requirements.txt
```

### Running Backend Tests

**Run all backend tests:**
```bash
npm run test:api
# or
pytest studio-api/tests/ -v
```

**Run specific test file:**
```bash
pytest studio-api/tests/test_router.py -v
```

**Run with coverage report:**
```bash
npm run test:api:coverage
# or
pytest studio-api/tests/ --cov=studio_api/studio_node --cov-report=html
```

**Run tests matching a pattern:**
```bash
pytest studio-api/tests/ -k "save" -v
```

### Backend Test Structure

```
studio-api/
├── main.py
├── studio_node/
│   ├── __init__.py
│   ├── router.py          # API endpoints
│   ├── service.py         # Business logic
│   └── schemas.py         # Data models
└── tests/
    ├── conftest.py        # Pytest fixtures
    ├── test_router.py     # Endpoint tests
    ├── test_service.py    # Service logic tests
    └── test_schemas.py    # Schema validation tests
```

### Backend Test Examples

**Testing API Endpoints:**
```python
def test_save_node_config(client, sample_payload):
    response = client.post("/api/v1/form-studio-node/save/form_123", json=sample_payload)
    assert response.status_code == 201
    assert response.json()["status"] == "success"
```

**Testing Business Logic:**
```python
def test_field_permission_resolution(validation_engine, sample_config):
    result = validation_engine.resolve_permissions(sample_config, "DRAFT")
    assert len(result["components"]) > 0
```

## 🎨 Frontend Testing

The frontend uses **Vitest** for unit tests and **Playwright** for E2E tests.

### Setup
```bash
# Test dependencies are in studio-ui/package.json and example-app/package.json
npm install --workspace=studio-ui
npm install --workspace=example-app
```

### Running Frontend Tests

**Run all frontend tests:**
```bash
npm run test:ui
```

**Run tests in watch mode (development):**
```bash
npm run test:ui:watch
```

**Run E2E tests:**
```bash
npm run test:e2e
```

**Run frontend with coverage:**
```bash
npm run test:ui:coverage
```

### Frontend Test Structure

```
studio-ui/
├── src/
│   ├── FormStudioNode/
│   │   ├── ButtonEdge.jsx
│   │   ├── index.jsx
│   │   ├── MatrixPanel.jsx
│   │   └── StateCanvasNode.jsx
│   └── __tests__/
│       ├── ButtonEdge.test.jsx
│       ├── MatrixPanel.test.jsx
│       └── StateCanvasNode.test.jsx
└── vitest.config.js

example-app/
├── src/
│   └── App.jsx
└── __tests__/
    └── App.test.jsx
```

## 🔄 Running All Tests

Run the complete test suite for both backend and frontend:

```bash
npm run test:all
```

This will:
1. Run backend tests with coverage
2. Run frontend unit tests
3. Run frontend E2E tests (if configured)
4. Generate combined coverage reports

## 📊 Test Coverage

### Check Coverage Reports

**Backend Coverage:**
```bash
pytest studio-api/tests/ --cov=studio_api/studio_node --cov-report=html
# Open htmlcov/index.html in browser
```

**Frontend Coverage:**
```bash
npm run test:ui:coverage --workspace=studio-ui
# Check coverage/ directory
```

### Coverage Goals
- **Statements:** ≥ 80%
- **Branches:** ≥ 75%
- **Functions:** ≥ 80%
- **Lines:** ≥ 80%

## 🔌 CI/CD Integration

### GitHub Actions (Example)

The test suite can be integrated into GitHub Actions:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: npm run install:all
      - run: npm run test:all
```

## 📝 Writing Tests

### Backend Test Template

Create files in `studio-api/tests/`:

```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_example(client):
    response = client.get("/api/v1/form-studio-node/runtime/form_1?instance_id=instance_01")
    assert response.status_code == 200
```

### Frontend Test Template

Create files in `studio-ui/src/__tests__/`:

```javascript
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ButtonEdge from '../FormStudioNode/ButtonEdge';

describe('ButtonEdge', () => {
  it('renders correctly', () => {
    render(<ButtonEdge data={{ label: 'Test' }} />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });
});
```

## 🐛 Debugging Tests

### Backend Debugging

```bash
# Run tests with verbose output
pytest studio-api/tests/ -vv

# Run single test with print statements
pytest studio-api/tests/test_router.py::test_specific_test -s

# Use pdb for debugging
pytest studio-api/tests/ --pdb
```

### Frontend Debugging

```bash
# Run tests in watch mode with UI
npm run test:ui:watch --workspace=studio-ui

# View browser when running E2E tests
npm run test:e2e -- --headed
```

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [Vitest Documentation](https://vitest.dev/)
- [Playwright Testing](https://playwright.dev/docs/intro)

## ✅ Pre-commit Checklist

Before committing, ensure:
- [ ] All tests pass: `npm run test:all`
- [ ] Coverage meets minimum thresholds
- [ ] No console errors in frontend tests
- [ ] No warnings in backend tests
- [ ] Code formatting is correct

## 🆘 Troubleshooting

### Tests not found
```bash
# Ensure test dependencies are installed
npm run install:all
pip install -r requirements.txt
```

### Port already in use (backend tests)
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Module not found errors
```bash
# Verify PYTHONPATH includes studio-api
export PYTHONPATH="${PYTHONPATH}:/workspaces/Form-Studio/studio-api"
```

### Frontend module errors
```bash
# Clear cache and reinstall
npm run clean
npm install
```
