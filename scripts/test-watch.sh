#!/bin/bash

# Color codes for output
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Running Backend Tests in Watch Mode${NC}"
echo "======================================="

cd studio-api

# Install requirements if needed
if ! command -v pytest &> /dev/null; then
    echo -e "${YELLOW}Installing test dependencies...${NC}"
    pip install -r ../requirements.txt
fi

# Run pytest in watch mode using pytest-watch if available, otherwise use --verbose
if command -v ptw &> /dev/null; then
    ptw tests/ -v
else
    echo -e "${YELLOW}For better watch mode, install pytest-watch: pip install pytest-watch${NC}"
    echo -e "${YELLOW}Running tests once. Re-run this command to test again.${NC}"
    python -m pytest tests/ -v --tb=short
fi
