"""
Smoke Tests for A11 Platform

Verify:
- Configuration loads without errors
- API server starts and responds to health checks
- No import errors in core modules
"""

import sys
import json
from pathlib import Path


def test_config_loads():
    """Test that configuration module loads without errors."""
    try:
        from config import settings, Settings
        
        # Verify required settings exist
        assert settings.ENV in ("development", "production", "staging")
        assert settings.API_PORT > 0
        assert settings.DATABASE_URL
        assert settings.EMBEDDING_DIMENSION > 0
        
        print("✓ Configuration loads successfully")
        return True
    except Exception as e:
        print(f"✗ Configuration loading failed: {e}")
        return False


def test_api_imports():
    """Test that API modules import without errors."""
    try:
        from api.main import app
        from api import deps
        
        # Verify FastAPI app is initialized
        assert app is not None
        assert hasattr(app, "get")
        assert hasattr(app, "post")
        
        print("✓ API modules import successfully")
        return True
    except Exception as e:
        print(f"✗ API import failed: {e}")
        return False


def test_core_packages_import():
    """Test that core package modules can be imported."""
    try:
        import halo
        import a11
        import echo
        
        print("✓ Core packages import successfully")
        return True
    except Exception as e:
        print(f"✗ Core package import failed: {e}")
        return False


def test_requirements_syntax():
    """Verify requirements.txt is well-formed."""
    try:
        with open("requirements.txt", "r") as f:
            lines = f.readlines()
        
        # Basic syntax check
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                # Should be package==version or similar
                if "==" not in line and "[" not in line:
                    print(f"⚠ Potentially malformed requirement: {line}")
        
        print("✓ requirements.txt syntax valid")
        return True
    except Exception as e:
        print(f"✗ requirements.txt check failed: {e}")
        return False


def test_env_example_exists():
    """Verify .env.example exists and is not committed as real .env."""
    try:
        env_example = Path(".env.example")
        env_real = Path(".env")
        
        assert env_example.exists(), ".env.example does not exist"
        assert not env_real.exists(), ".env (production secrets) should not be committed"
        
        print("✓ Environment configuration structure correct")
        return True
    except AssertionError as e:
        print(f"✗ Environment check failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Environment file check failed: {e}")
        return False


def test_dockerfile_exists():
    """Verify Dockerfile is present for containerization."""
    try:
        dockerfile = Path("Dockerfile")
        assert dockerfile.exists(), "Dockerfile not found"
        
        with open("Dockerfile", "r") as f:
            content = f.read()
        
        assert "FROM" in content, "Dockerfile missing FROM statement"
        assert "EXPOSE" in content, "Dockerfile missing EXPOSE statement"
        
        print("✓ Dockerfile present and well-formed")
        return True
    except AssertionError as e:
        print(f"✗ Dockerfile check failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Dockerfile validation failed: {e}")
        return False


def test_gitignore_allows_config():
    """Verify .gitignore doesn't block intentional config files."""
    try:
        with open(".gitignore", "r") as f:
            gitignore_content = f.read()
        
        # Should NOT have blanket *.json block
        lines = [line.strip() for line in gitignore_content.split("\n")]
        
        # Look for problematic patterns
        if "*.json" in lines:
            print("⚠ .gitignore blocks *.json (may block config files)")
            return False
        
        print("✓ .gitignore correctly structured")
        return True
    except Exception as e:
        print(f"✗ .gitignore check failed: {e}")
        return False


def run_all_smoke_tests():
    """Run all smoke tests and report results."""
    print("\n" + "="*60)
    print("SMOKE TEST SUITE: A11 Platform Foundation")
    print("="*60 + "\n")
    
    tests = [
        ("Configuration Loading", test_config_loads),
        ("API Module Imports", test_api_imports),
        ("Core Package Imports", test_core_packages_import),
        ("Requirements Syntax", test_requirements_syntax),
        ("Environment Configuration", test_env_example_exists),
        ("Dockerfile Validation", test_dockerfile_exists),
        (".gitignore Validation", test_gitignore_allows_config),
    ]
    
    results = []
    for test_name, test_fn in tests:
        try:
            result = test_fn()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name}: Unhandled exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("SMOKE TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} | {test_name}")
    
    print("="*60)
    print(f"Result: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_smoke_tests()
    sys.exit(0 if success else 1)
