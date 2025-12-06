# TruEstate - Makefile for cross-platform development

.PHONY: help setup install seed dev test lint format clean docker-up docker-down

help: ## Show this help message
	@echo "TruEstate Development Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Setup & Installation
setup: ## Initial project setup
	@echo "Setting up TruEstate..."
	cd backend && python -m venv venv
	@echo "Activate venv: backend/venv/Scripts/activate (Windows) or source backend/venv/bin/activate (Unix)"
	$(MAKE) install

install: ## Install all dependencies
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

# Database
seed: ## Seed the database with sample data
	@echo "Seeding database..."
	cd backend && python scripts/seed_db.py 500

# Development
dev-backend: ## Run backend development server
	cd backend && uvicorn src.index:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Run frontend development server
	cd frontend && npm run dev

dev: ## Run both backend and frontend (requires split terminal)
	@echo "Run 'make dev-backend' in one terminal and 'make dev-frontend' in another"

# Testing
test-backend: ## Run backend tests
	cd backend && pytest --cov=src --cov-report=html --cov-report=term-missing

test-frontend: ## Run frontend tests
	cd frontend && npm run test:coverage

test: ## Run all tests
	$(MAKE) test-backend
	$(MAKE) test-frontend

# Linting & Formatting
lint-backend: ## Lint backend code
	cd backend && ruff check src tests
	cd backend && black --check src tests

lint-frontend: ## Lint frontend code
	cd frontend && npm run lint
	cd frontend && npx tsc --noEmit

lint: ## Lint all code
	$(MAKE) lint-backend
	$(MAKE) lint-frontend

format-backend: ## Format backend code
	cd backend && black src tests
	cd backend && isort src tests

format-frontend: ## Format frontend code
	cd frontend && npx prettier --write "src/**/*.{ts,tsx,css}"

format: ## Format all code
	$(MAKE) format-backend
	$(MAKE) format-frontend

# Building
build-frontend: ## Build frontend for production
	cd frontend && npm run build

# Docker
docker-up: ## Start all services with Docker Compose
	docker-compose up -d

docker-down: ## Stop all Docker services
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

docker-rebuild: ## Rebuild and restart Docker services
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d

# Cleanup
clean: ## Clean build artifacts and cache
	@echo "Cleaning..."
	cd backend && rm -rf __pycache__ .pytest_cache .coverage htmlcov *.db
	cd frontend && rm -rf node_modules dist coverage
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Verification
verify: ## Run all verification checks
	@echo "Running verification checks..."
	$(MAKE) lint
	$(MAKE) test
	cd backend && python scripts/verify_no_pydantic_warnings.py
	@echo "✅ All checks passed!"
