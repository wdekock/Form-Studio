# Testing Scripts

This directory contains convenient shell scripts for running tests on the Form Studio project.

## Quick Start

```bash
# Run all tests (backend + frontend)
bash scripts/test-all.sh

# Run only backend tests
bash scripts/test-backend.sh

# Generate coverage report
bash scripts/test-coverage.sh

# Run tests in watch mode (re-runs on file changes)
bash scripts/test-watch.sh
```

## Scripts Overview

### `test-backend.sh`
Runs all Python backend tests using pytest.

**Features:**
- Automatically installs pytest if missing
- Shows verbose output with test names
- Clear pass/fail indicators

**Usage:**
```bash
bash scripts/test-backend.sh
```

### `test-coverage.sh`
Runs backend tests and generates a coverage report showing which code is tested.

**Output:**
- Terminal report showing coverage percentages
- HTML report in `studio-api/htmlcov/index.html`

**Usage:**
```bash
bash scripts/test-coverage.sh
# Then open studio-api/htmlcov/index.html in a browser
```

### `test-all.sh`
Runs both backend and frontend tests with a summary report.

**Features:**
- Tests backend (Python/FastAPI)
- Tests frontend (React) if configured
- Shows summary of all test results
- Returns appropriate exit code for CI/CD

**Usage:**
```bash
bash scripts/test-all.sh
```

### `test-watch.sh`
Runs backend tests in watch mode, automatically re-running when files change.

**Features:**
- Watches for file changes in studio-api
- Automatically re-runs affected tests
- Better for development workflow

**Installation:**
```bash
# For better watch mode experience, install pytest-watch:
pip install pytest-watch
```

**Usage:**
```bash
bash scripts/test-watch.sh
```

## Direct npm Commands

You can also use npm scripts directly:

```bash
# Backend tests
npm run test:api              # Run backend tests
npm run test:api:coverage     # Generate coverage report

# Frontend tests  
npm run test:ui               # Run all frontend tests
npm run test:ui:watch         # Watch mode for frontend
npm run test:ui:coverage      # Frontend coverage report

# All tests
npm run test:all              # Run backend + frontend tests
```

## Making Scripts Executable

On Unix-like systems (Linux, macOS):

```bash
chmod +x scripts/*.sh
```

Then you can run them without `bash`:
```bash
./scripts/test-backend.sh
./scripts/test-coverage.sh
```

## Integration with CI/CD

These scripts return appropriate exit codes for CI/CD pipelines:
- Exit code `0` = all tests passed ✅
- Exit code `1` = tests failed ❌

Example GitHub Actions:
```yaml
- name: Run Tests
  run: bash scripts/test-all.sh
```

## Troubleshooting

**pytest not found:**
```bash
pip install -r requirements.txt
```

**Permission denied:**
```bash
chmod +x scripts/test-backend.sh
```

**Port already in use (for integration tests):**
```bash
lsof -ti:8000 | xargs kill -9
```

## Requirements

- Python 3.8+
- pytest >= 7.4.4
- pytest-cov >= 4.1.0
- pytest-asyncio >= 0.23.2

All dependencies are listed in `/requirements.txt`
