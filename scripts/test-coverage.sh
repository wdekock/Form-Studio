#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📊 Generating Backend Test Coverage Report...${NC}"
echo "=================================================="

# Check if pytest-cov is installed
if ! pip show pytest-cov &> /dev/null; then
    echo -e "${YELLOW}Installing pytest-cov...${NC}"
    pip install pytest-cov
fi

cd studio-api

# Run tests with coverage
python -m pytest tests/ \
    --cov=studio_node \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-report=term \
    -v

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo -e "\n${GREEN}✅ Coverage report generated!${NC}"
    echo -e "${BLUE}📂 Report location: $(pwd)/htmlcov/index.html${NC}"
    echo -e "${YELLOW}View it by opening the HTML file in your browser${NC}"
else
    echo -e "\n${RED}❌ Coverage generation failed!${NC}"
fi

exit $exit_code
