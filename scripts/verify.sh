#!/bin/bash
# A11 Platform Local Verification Script
# Runs all checks: format, lint, type, tests, smoke tests

set -e

echo "================================"
echo "A11 Platform: Local Verification"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python --version
echo ""

# 1. Format check with Black
echo "1. Format check (black)..."
black --check . --exclude venv,node_modules || {
    echo "Run: black . --exclude venv,node_modules"
    exit 1
}
echo "✓ Format check passed"
echo ""

# 2. Lint check with Ruff
echo "2. Lint check (ruff)..."
ruff check . || {
    echo "Run: ruff check . --fix"
    exit 1
}
echo "✓ Lint check passed"
echo ""

# 3. Type check with mypy
echo "3. Type check (mypy)..."
mypy config.py api/ --ignore-missing-imports || {
    echo "⚠ Type check found issues (non-blocking)"
}
echo "✓ Type check complete"
echo ""

# 4. Smoke tests
echo "4. Smoke tests..."
python tests/test_smoke.py
echo ""

# 5. Unit tests
echo "5. Unit tests (pytest)..."
pytest tests/ -v --tb=short || {
    echo "Some tests failed"
    exit 1
}
echo "✓ Unit tests passed"
echo ""

echo "================================"
echo "✓ All checks passed"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Review changes: git status"
echo "2. Stage changes: git add ."
echo "3. Commit: git commit -m 'message'"
echo "4. Push: git push origin branch-name"
