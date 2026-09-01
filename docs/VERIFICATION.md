# A11 Platform Local Verification Procedures

## Prerequisites

- Python 3.11+
- pip
- Docker & Docker Compose (optional, for containerized testing)
- git

## Environment Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create .env from Template

```bash
cp .env.example .env
# Edit .env with your local values (not needed for smoke tests)
```

## Running Verification Checks

### Quick Smoke Tests (No External Services)

```bash
python tests/test_smoke.py
```

**What it verifies:**
- Configuration module loads
- API modules import correctly
- Core packages import
- requirements.txt syntax
- Environment files structure
- Dockerfile is valid
- .gitignore doesn't block config files

**Expected output:**
```
============================================================
SMOKE TEST SUITE: A11 Platform Foundation
============================================================

✓ Configuration Loading
✓ API Module Imports
✓ Core Package Imports
✓ Requirements Syntax
✓ Environment Configuration
✓ Dockerfile Validation
.gitignore Validation

============================================================
SMOKE TEST SUMMARY
============================================================
✓ PASS | Configuration Loading
✓ PASS | API Module Imports
✓ PASS | Core Package Imports
✓ PASS | Requirements Syntax
✓ PASS | Environment Configuration
✓ PASS | Dockerfile Validation
✓ PASS | .gitignore Validation
============================================================
Result: 7/7 tests passed
============================================================
```

### Full Local Verification

```bash
bash scripts/verify.sh
```

**Runs:**
1. Black code formatting check
2. Ruff linting
3. mypy type checking
4. Smoke tests
5. pytest unit tests

### API Server Locally (Without Docker)

```bash
# Terminal 1: Start PostgreSQL + Redis
docker-compose up postgres redis

# Terminal 2: Run API server
python -m api.main
```

**Verify:**
```bash
# In another terminal
curl http://localhost:8000/health
curl http://localhost:8000/ready
```

### Docker Verification

```bash
# Build and test in Docker
bash scripts/docker-verify.sh
```

Or manually:

```bash
# Build
docker build -t a11-platform:latest .

# Run smoke tests
docker run --rm a11-platform:latest python tests/test_smoke.py

# Run full stack with compose
docker-compose up
```

## Verification Results

### Current Status (Sept 1, 2026)

**✓ Implemented & Verified:**
- Configuration system (config.py)
- FastAPI application skeleton with health checks
- Docker containerization
- Test framework (pytest)
- Smoke test suite (7/7 passing)
- Requirements locked to specific versions
- .gitignore fixed to allow config files
- Project structure with placeholders for core modules

**⚠ Not Yet Implemented:**
- Halo ingestion service (placeholder packages exist)
- A11 query engine (placeholder packages exist)
- Echo governance layer (placeholder packages exist)
- Database schema and migrations
- API endpoints (health checks only)
- GTM artifact generation runner
- External service integrations (Gemini API, BigQuery, etc.)

**🔒 Not Attempted (Blocked - Requires Secrets):**
- Gemini API integration (requires GEMINI_API_KEY)
- BigQuery connection (requires GCP credentials)
- Google Cloud deployment
- Live LLM model routing

## Failed Checks & Fixes

### Issue: .gitignore blocked *.json files

**Status:** ✓ FIXED

- **Problem:** Line `*.json` blocked all JSON files, including skill-lock.json and config manifests
- **Fix:** Removed blanket block, keeps only credential files (.key, .pem, gcp-key.json)
- **Verification:** `test_gitignore_allows_config()` now passes

### Issue: Missing api/main.py referenced in docker-compose.yml

**Status:** ✓ FIXED

- **Problem:** docker-compose.yml called `uvicorn api.main:app` but file didn't exist
- **Fix:** Created api/main.py with FastAPI app and health endpoints
- **Verification:** `test_api_imports()` now passes

### Issue: Dockerfile missing from repository

**Status:** ✓ FIXED

- **Problem:** docker-compose.yml referenced `Dockerfile` but it didn't exist
- **Fix:** Added production-grade Dockerfile with non-root user, health checks, security best practices
- **Verification:** `test_dockerfile_exists()` now passes

### Issue: No core package structure

**Status:** ✓ FIXED (Placeholders)

- **Problem:** README referenced halo/, a11/, echo/ but packages didn't exist
- **Fix:** Added __init__.py placeholders for all three core packages
- **Verification:** `test_core_packages_import()` now passes

### Issue: No test infrastructure

**Status:** ✓ FIXED

- **Problem:** tests/ folder empty, no pytest configuration
- **Fix:** Added pyproject.toml, conftest.py, smoke tests, API tests, config tests
- **Verification:** All pytest runs pass

## Next Steps

1. **Implement Halo ingestion service** (placeholder exists, needs implementation)
2. **Add database schema** (DDL for document_chunks, evidence_log)
3. **Implement A11 query engine** (placeholder exists, needs hybrid search + multi-model routing)
4. **Add Echo governance layer** (placeholder exists, needs rules engine + logging)
5. **Create CI/CD pipeline** (GitHub Actions for lint, test, build)
6. **Test with real Gemini API** (requires GEMINI_API_KEY)

## Troubleshooting

### "ModuleNotFoundError: No module named 'config'"

Run: `pip install -r requirements.txt`

### "postgres connection refused"

Run: `docker-compose up postgres` in another terminal

### "black check failed"

Run: `black . --exclude venv,node_modules`

### "ruff found issues"

Run: `ruff check . --fix`

### Tests fail with "Cannot import name 'TestClient'"

Run: `pip install -r requirements.txt` (testclient is in dependencies)

---

**Last Updated:** Sept 1, 2026
**Status:** Foundation audit complete, core issues fixed, ready for feature implementation
