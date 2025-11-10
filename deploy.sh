#!/bin/bash

# NewsFlow Deployment Script
# This script helps with deployment to production

set -e

echo "🚀 NewsFlow Deployment Script"
echo "=============================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Functions
print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check prerequisites
print_step "Checking prerequisites..."

if ! command -v git &> /dev/null; then
    print_error "Git not found. Please install Git."
    exit 1
fi

print_success "Prerequisites check passed"
echo ""

# Menu
echo "Select deployment target:"
echo "1) Backend to Render"
echo "2) Frontend to Vercel"
echo "3) Full deployment (Backend + Frontend)"
echo "4) Run tests before deployment"
echo "5) Exit"
read -p "Enter choice [1-5]: " deploy_choice

case $deploy_choice in
    1)
        print_step "Deploying Backend to Render..."
        
        # Check if .env exists
        if [ ! -f backend/.env ]; then
            print_error "backend/.env not found!"
            print_warning "Please create backend/.env with production values"
            exit 1
        fi
        
        # Run tests
        print_step "Running backend tests..."
        cd backend
        source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
        pytest || {
            print_error "Tests failed! Fix errors before deploying."
            exit 1
        }
        cd ..
        
        print_success "Tests passed!"
        
        # Commit and push
        print_step "Committing changes..."
        git add .
        git commit -m "Deploy: Backend update $(date +%Y-%m-%d)" || print_warning "Nothing to commit"
        
        print_step "Pushing to main..."
        git push origin main
        
        print_success "Backend deployed!"
        print_warning "Check Render dashboard for deployment status"
        ;;
        
    2)
        print_step "Deploying Frontend to Vercel..."
        
        # Build frontend
        print_step "Building frontend..."
        cd frontend
        npm run build -- --configuration production || {
            print_error "Build failed!"
            exit 1
        }
        cd ..
        
        print_success "Build successful!"
        
        # Check if vercel CLI is installed
        if ! command -v vercel &> /dev/null; then
            print_warning "Vercel CLI not found. Installing..."
            npm install -g vercel
        fi
        
        # Deploy
        print_step "Deploying to Vercel..."
        cd frontend
        vercel --prod
        cd ..
        
        print_success "Frontend deployed!"
        ;;
        
    3)
        print_step "Full deployment..."
        
        # Run tests
        print_step "Running all tests..."
        
        # Backend tests
        cd backend
        source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
        pytest || {
            print_error "Backend tests failed!"
            exit 1
        }
        cd ..
        
        # Frontend tests
        cd frontend
        npm run test -- --watch=false || {
            print_error "Frontend tests failed!"
            exit 1
        }
        cd ..
        
        print_success "All tests passed!"
        
        # Commit and push
        print_step "Committing changes..."
        git add .
        git commit -m "Deploy: Full update $(date +%Y-%m-%d)" || print_warning "Nothing to commit"
        git push origin main
        
        # Deploy frontend
        print_step "Deploying frontend..."
        cd frontend
        vercel --prod
        cd ..
        
        print_success "Full deployment completed!"
        print_warning "Check Render and Vercel dashboards for status"
        ;;
        
    4)
        print_step "Running all tests..."
        
        # Backend tests
        print_step "Backend tests..."
        cd backend
        source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
        pytest -v
        cd ..
        
        # Frontend tests
        print_step "Frontend tests..."
        cd frontend
        npm run test -- --watch=false
        cd ..
        
        print_success "All tests completed!"
        ;;
        
    5)
        echo "Exiting..."
        exit 0
        ;;
        
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✨ Deployment complete!${NC}"
echo ""
echo "Next steps:"
echo "- Check deployment status on hosting platforms"
echo "- Test production URLs"
echo "- Monitor logs for errors"
echo ""

