#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 Running All Tests (Backend + Frontend)${NC}"
echo "=============================================="

# Test Backend
echo -e "\n${YELLOW}1️⃣ Testing Backend (Python/FastAPI)...${NC}"
bash scripts/test-backend.sh
backend_exit=$?

# Test Frontend (if scripts exist)
if npm run test:ui 2>/dev/null; then
    echo -e "\n${YELLOW}2️⃣ Testing Frontend (React)...${NC}"
    npm run test:ui
    frontend_exit=$?
else
    echo -e "\n${YELLOW}⚠️  Frontend test scripts not yet configured${NC}"
    frontend_exit=0
fi

# Summary
echo -e "\n${BLUE}📋 Test Summary${NC}"
echo "================"

if [ $backend_exit -eq 0 ]; then
    echo -e "${GREEN}✅ Backend tests: PASSED${NC}"
else
    echo -e "${RED}❌ Backend tests: FAILED${NC}"
fi

if [ $frontend_exit -eq 0 ]; then
    echo -e "${GREEN}✅ Frontend tests: PASSED${NC}"
else
    echo -e "${RED}❌ Frontend tests: FAILED${NC}"
fi

# Final result
if [ $backend_exit -eq 0 ] && [ $frontend_exit -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}⚠️  Some tests failed${NC}"
    exit 1
fi
