#!/bin/bash

# Local testing script for NewsFlow

echo "🧪 NewsFlow Local Testing"
echo "========================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test Backend
echo -e "${YELLOW}Testing Backend...${NC}"
cd backend

# Activate virtual environment
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# Run pytest
pytest -v --tb=short

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend tests passed!${NC}"
else
    echo -e "${RED}✗ Backend tests failed!${NC}"
    exit 1
fi

cd ..

# Test Frontend
echo ""
echo -e "${YELLOW}Testing Frontend...${NC}"
cd frontend

# Run Angular tests
npm run test -- --watch=false --browsers=ChromeHeadless

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Frontend tests passed!${NC}"
else
    echo -e "${RED}✗ Frontend tests failed!${NC}"
    exit 1
fi

cd ..

echo ""
echo -e "${GREEN}✨ All tests passed!${NC}"
echo ""

# Optional: Start services
read -p "Do you want to start the services? (y/n): " start_services

if [ "$start_services" = "y" ]; then
    echo ""
    echo "Starting services..."
    docker-compose up -d
    
    echo ""
    echo "Services started!"
    echo "- Frontend: http://localhost:4200"
    echo "- Backend: http://localhost:8000"
    echo "- API Docs: http://localhost:8000/api/docs"
    echo ""
    echo "Press Ctrl+C to stop watching logs"
    docker-compose logs -f
fi

