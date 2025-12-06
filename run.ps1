# TruEstate PowerShell Helper Script for Windows

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "TruEstate Development Commands:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Setup & Installation:" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 setup          - Initial project setup"
    Write-Host "  .\run.ps1 install        - Install all dependencies"
    Write-Host ""
    Write-Host "Database:" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 seed           - Seed database with sample data"
    Write-Host ""
    Write-Host "Development:" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 dev-backend    - Run backend dev server"
    Write-Host "  .\run.ps1 dev-frontend   - Run frontend dev server"
    Write-Host ""
    Write-Host "Testing:" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 test-backend   - Run backend tests"
    Write-Host "  .\run.ps1 test-frontend  - Run frontend tests"
    Write-Host "  .\run.ps1 test           - Run all tests"
    Write-Host ""
    Write-Host "Linting:" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 lint-backend   - Lint backend code"
    Write-Host "  .\run.ps1 lint-frontend  - Lint frontend code"
    Write-Host "  .\run.ps1 lint           - Lint all code"
    Write-Host ""
    Write-Host "Docker:" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 docker-up      - Start Docker services"
    Write-Host "  .\run.ps1 docker-down    - Stop Docker services"
    Write-Host ""
    Write-Host "Cleanup:" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 clean          - Clean build artifacts"
}

switch ($Command) {
    "setup" {
        Write-Host "Setting up TruEstate..." -ForegroundColor Green
        Set-Location backend
        python -m venv venv
        Write-Host "Activate venv: .\backend\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
        Set-Location ..
        & $PSCommandPath install
    }
    
    "install" {
        Write-Host "Installing dependencies..." -ForegroundColor Green
        Set-Location backend
        pip install -r requirements.txt
        Set-Location ..\frontend
        npm install
        Set-Location ..
    }
    
    "seed" {
        Write-Host "Seeding database..." -ForegroundColor Green
        Set-Location backend
        python scripts\seed_db.py 500
        Set-Location ..
    }
    
    "dev-backend" {
        Write-Host "Starting backend dev server..." -ForegroundColor Green
        Set-Location backend
        uvicorn src.index:app --reload --host 0.0.0.0 --port 8000
    }
    
    "dev-frontend" {
        Write-Host "Starting frontend dev server..." -ForegroundColor Green
        Set-Location frontend
        npm run dev
    }
    
    "test-backend" {
        Write-Host "Running backend tests..." -ForegroundColor Green
        Set-Location backend
        pytest --cov=src --cov-report=html --cov-report=term-missing
        Set-Location ..
    }
    
    "test-frontend" {
        Write-Host "Running frontend tests..." -ForegroundColor Green
        Set-Location frontend
        npm run test:coverage
        Set-Location ..
    }
    
    "test" {
        & $PSCommandPath test-backend
        & $PSCommandPath test-frontend
    }
    
    "lint-backend" {
        Write-Host "Linting backend..." -ForegroundColor Green
        Set-Location backend
        ruff check src tests
        black --check src tests
        Set-Location ..
    }
    
    "lint-frontend" {
        Write-Host "Linting frontend..." -ForegroundColor Green
        Set-Location frontend
        npm run lint
        Set-Location ..
    }
    
    "lint" {
        & $PSCommandPath lint-backend
        & $PSCommandPath lint-frontend
    }
    
    "docker-up" {
        Write-Host "Starting Docker services..." -ForegroundColor Green
        docker-compose up -d
    }
    
    "docker-down" {
        Write-Host "Stopping Docker services..." -ForegroundColor Green
        docker-compose down
    }
    
    "clean" {
        Write-Host "Cleaning build artifacts..." -ForegroundColor Green
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue backend\__pycache__
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue backend\.pytest_cache
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue backend\htmlcov
        Remove-Item -Force -ErrorAction SilentlyContinue backend\*.db
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue frontend\node_modules
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue frontend\dist
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue frontend\coverage
    }
    
    default {
        Show-Help
    }
}
