#!/bin/bash
# A11 Platform Docker Local Verification
# Builds and runs the Docker container locally

set -e

echo "================================"
echo "A11 Docker Build & Verification"
echo "================================"
echo ""

# Build the Docker image
echo "Building Docker image..."
docker build -t a11-platform:latest .
echo "✓ Docker image built"
echo ""

# Run smoke tests in container
echo "Running smoke tests in container..."
docker run --rm a11-platform:latest python tests/test_smoke.py
echo "✓ Container smoke tests passed"
echo ""

echo "================================"
echo "✓ Docker verification passed"
echo "================================"
