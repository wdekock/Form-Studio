#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🧪 Starting Backend Tests...${NC}"
echo "=================================="

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}❌ pytest is not installed. Running: pip install -r requirements.txt${NC}"
    pip install -r requirements.txt
fi

# Run tests
cd studio-api
python -m pytest tests/ -v --tb=short

# Capture exit code
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo -e "\n${GREEN}✅ All tests passed!${NC}"
else
    echo -e "\n${RED}❌ Some tests failed!${NC}"
fi

exit $exit_code
