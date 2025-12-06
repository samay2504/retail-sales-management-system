# TruEstate - Retail Sales Management System

[![Backend CI](https://github.com/samay2504/retail-sales-management-system/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/samay2504/retail-sales-management-system/actions/workflows/backend-ci.yml)
[![Frontend CI](https://github.com/samay2504/retail-sales-management-system/actions/workflows/frontend-ci.yml/badge.svg)](https://github.com/samay2504/retail-sales-management-system/actions/workflows/frontend-ci.yml)
[![Deploy](https://github.com/samay2504/retail-sales-management-system/actions/workflows/deploy-gh-pages.yml/badge.svg)](https://github.com/samay2504/retail-sales-management-system/actions/workflows/deploy-gh-pages.yml)

A modern, production-ready retail sales management system with advanced search, filtering, and analytics capabilities.

**🚀 Live Application**: [https://samay2504.github.io/retail-sales-management-system](https://samay2504.github.io/retail-sales-management-system)

**📚 Production Setup**: 
- [DEPLOYMENT.md](DEPLOYMENT.md) - General deployment guide
- [RENDER_DEPLOY.md](RENDER_DEPLOY.md) - Render-specific configuration

---

## Overview

TruEstate is a full-stack web application designed for managing retail sales transactions with powerful search and filtering capabilities. Built with modern technologies and best practices, it provides:

- **Full-text search** across customer names and phone numbers
- **Advanced filtering** with multi-select and range filters
- **Flexible sorting** by date, quantity, and customer name
- **Efficient pagination** with 10 items per page
- **Real-time caching** for optimal performance
- **Responsive design** with dark theme and glassmorphism UI

---

## Tech Stack

### Backend
- **Framework**: FastAPI 0.109+ (Python 3.11+)
- **Database**: SQLite with FTS5 (dev), PostgreSQL (production)
- **ORM**: SQLAlchemy 2.0 (async)
- **Validation**: Pydantic v2
- **Caching**: In-memory (cachetools) or Redis
- **Testing**: pytest, pytest-asyncio
- **Deployment**: Docker, Railway/Render/Fly.io

### Frontend
- **Framework**: React 18 with TypeScript 5
- **Build Tool**: Vite 5
- **Styling**: Tailwind CSS 3.4 with custom dark theme
- **State Management**: TanStack Query (React Query) v5
- **HTTP Client**: Axios
- **Testing**: Vitest, Testing Library
- **Deployment**: GitHub Pages

### DevOps
- **CI/CD**: GitHub Actions
- **Containerization**: Docker, Docker Compose
- **Development**: VS Code DevContainer
- **Cross-platform**: Makefile + PowerShell scripts

---

## Search Implementation Summary

### Search Engine: SQLite FTS5

**Technology**: SQLite Full-Text Search 5 (FTS5) virtual table

**Searchable Fields**:
- Customer Name (full-text)
- Phone Number (exact and partial match)

**Algorithm**:
1. User input normalized (lowercase, whitespace stripped)
2. FTS5 MATCH query against virtual table
3. Results joined with main transactions table
4. Combined with active filters and sorting
5. Cached for 30 seconds

**Features**:
- Case-insensitive search
- Partial word matching
- Fast indexing and retrieval
- No external dependencies

**Performance**: 
- < 50ms for typical searches on 10,000+ records
- FTS index automatically maintained on inserts/updates

**Alternative**: PostgreSQL with `pg_trgm` and `GIN` indexes documented in `/docs/architecture.md`

---

## Filter Implementation Summary

### Multi-Select Filters

Implemented using SQL `IN` clauses with array parameters:

- **Customer Region**: North, South, East, West, Central
- **Gender**: Male, Female, Other
- **Product Category**: Electronics, Clothing, Food & Beverage, etc.
- **Tags**: bestseller, clearance, premium, seasonal, etc.
- **Payment Method**: Credit Card, Debit Card, Cash, Digital Wallet, Bank Transfer

**Query Construction**:
```sql
WHERE customer_region IN ('North', 'South')
  AND payment_method IN ('Credit Card', 'Cash')
```

### Range Filters

Implemented using SQL comparison operators:

- **Age Range**: Min/Max integer values
  ```sql
  WHERE age >= 25 AND age <= 45
  ```

- **Date Range**: ISO date strings (YYYY-MM-DD)
  ```sql
  WHERE date >= '2024-01-01' AND date <= '2024-12-31'
  ```

### Filter Metadata Endpoint

`GET /api/meta/filters` returns:
- Unique values for each filterable field
- Count of transactions per value
- Min/max ranges for age and dates

**Optimization**:
- Indexed columns for fast filtering
- Cached metadata for 5 minutes
- Single query retrieves all filter options with counts

---

## Sorting Implementation Summary

### Supported Sort Fields

1. **Date** (default: newest first)
   - `date:desc` - Newest to oldest
   - `date:asc` - Oldest to newest

2. **Quantity**
   - `quantity:desc` - Highest to lowest
   - `quantity:asc` - Lowest to highest

3. **Customer Name**
   - `customer_name:asc` - A to Z
   - `customer_name:desc` - Z to A

### Implementation

**Query Parameter**: `?sort=field:direction`

**SQL Generation**:
```python
ORDER BY {field} {ASC|DESC}
```

**Index Optimization**: 
- Indexed on `date`, `quantity`, `customer_name`
- Composite indexes for common sort + filter combinations

**With Search**: 
- Relevance scoring available when search query present
- Explicit sort parameter overrides relevance ordering

**State Preservation**:
- Sort selection retained across filter changes
- Persisted in React Query cache

---

## Pagination Implementation Summary

### Configuration

- **Page Size**: 10 items per page (default)
- **Max Limit**: 100 items per page
- **Type**: Offset-based (configurable to cursor-based)

### API Parameters

- `page`: 1-indexed page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)

### Response Metadata

```json
{
  "items": [...],
  "meta": {
    "total": 500,
    "page": 2,
    "limit": 10,
    "total_pages": 50,
    "has_next": true,
    "has_prev": true
  }
}
```

### Implementation

**SQL Query**:
```sql
LIMIT 10 OFFSET 10  -- Page 2
```

**Optimization**:
- Single query retrieves count + results
- Cursor-based pagination available for large datasets (docs in `/docs/architecture.md`)

**State Management**:
- Page state maintained in React component
- Search/filter/sort state preserved across page navigation
- React Query caches each page independently

**UI Features**:
- Previous/Next buttons with disabled states
- Page number buttons (with ellipsis for large ranges)
- Mobile-friendly pagination controls
- Results summary: "Showing 11-20 of 500 results"

---

## Setup Instructions

### Prerequisites

- **Python 3.11+** (for backend)
- **Node.js 20+** (for frontend)
- **Docker** (optional, for containerized deployment)
- **Git**

### Quick Start (All Platforms)

#### Windows (PowerShell)

```powershell
# 1. Clone repository
git clone https://github.com/yourusername/truestate.git
cd truestate

# 2. Setup and install dependencies
.\run.ps1 setup
.\run.ps1 install

# 3. Seed database
.\run.ps1 seed

# 4. Run backend (in first terminal)
.\run.ps1 dev-backend

# 5. Run frontend (in second terminal)
.\run.ps1 dev-frontend
```

#### macOS / Linux (Make)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/truestate.git
cd truestate

# 2. Setup and install dependencies
make setup
make install

# 3. Seed database
make seed

# 4. Run backend (in first terminal)
make dev-backend

# 5. Run frontend (in second terminal)
make dev-frontend
```

### Application URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

---

### Backend Setup (Detailed)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows: .\venv\Scripts\activate
# Unix: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Seed database with 500 sample transactions
python scripts/seed_db.py 500

# Run development server
uvicorn src.index:app --reload --host 0.0.0.0 --port 8000
```

**Backend Tests**:
```bash
pytest
pytest --cov=src --cov-report=html  # With coverage
```

---

### Frontend Setup (Detailed)

```bash
cd frontend

# Install dependencies
npm install

# Create .env file (optional for production API URL)
cp .env.example .env

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

**Frontend Tests**:
```bash
npm run test
npm run test:coverage  # With coverage
```

---

### Docker Setup

Run full stack with Docker Compose:

```bash
# Start all services (backend + Redis)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# With PostgreSQL (optional)
docker-compose --profile postgres up -d
```

Services:
- Backend: http://localhost:8000
- Redis: localhost:6379
- PostgreSQL: localhost:5432 (if using postgres profile)

---

### VS Code DevContainer

Open project in VS Code and select "Reopen in Container" when prompted, or:

```
Ctrl+Shift+P → "Dev Containers: Reopen in Container"
```

Everything will be set up automatically with pre-seeded database.

---

## Project Structure

```
TueEstate/
├── backend/              # FastAPI backend
│   ├── src/
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── routes/       # API endpoints
│   │   └── utils/        # Utilities
│   ├── scripts/          # Database seeding, etc.
│   ├── tests/            # pytest tests
│   └── requirements.txt
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom hooks
│   │   ├── services/     # API client
│   │   └── types/        # TypeScript types
│   ├── tests/            # Vitest tests
│   └── package.json
├── docs/                 # Documentation
│   └── architecture.md   # Architecture details
├── .github/workflows/    # CI/CD pipelines
├── docker-compose.yml    # Docker orchestration
├── Makefile              # Build automation
├── run.ps1               # Windows helper
└── README.md             # This file
```

---

## Development Commands

### Makefile (macOS/Linux)

```bash
make help              # Show all commands
make install           # Install all dependencies
make seed              # Seed database
make dev-backend       # Run backend dev server
make dev-frontend      # Run frontend dev server
make test              # Run all tests
make lint              # Lint all code
make format            # Format all code
make docker-up         # Start Docker services
make clean             # Clean build artifacts
```

### PowerShell (Windows)

```powershell
.\run.ps1 help         # Show all commands
.\run.ps1 install      # Install all dependencies
.\run.ps1 seed         # Seed database
.\run.ps1 dev-backend  # Run backend dev server
.\run.ps1 dev-frontend # Run frontend dev server
.\run.ps1 test         # Run all tests
.\run.ps1 lint         # Lint all code
.\run.ps1 docker-up    # Start Docker services
.\run.ps1 clean        # Clean build artifacts
```

---

## API Endpoints

### Transactions

- `GET /api/transactions` - List transactions with search, filters, sort, pagination
  - Query params: `q`, `page`, `limit`, `sort`, `customer_region[]`, `gender[]`, `product_category[]`, `tags[]`, `payment_method[]`, `age_min`, `age_max`, `date_from`, `date_to`
  
- `GET /api/transactions/{id}` - Get single transaction

### Metadata

- `GET /api/meta/filters` - Get filter options with counts
- `GET /api/health` - Health check

### Documentation

- `GET /api/docs` - Interactive Swagger UI
- `GET /api/redoc` - ReDoc documentation

---

## Deployment

### Backend Deployment

**Option 1: Railway** (Recommended)
1. Create account at [railway.app](https://railway.app)
2. Click "Deploy from GitHub"
3. Select repository and `backend` directory
4. Set environment variables
5. Deploy

**Option 2: Render**
1. Create account at [render.com](https://render.com)
2. New Web Service → Connect repository
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn src.index:app --host 0.0.0.0 --port $PORT`

**Option 3: Docker**
```bash
cd backend
docker build -t truestate-backend .
docker run -p 8000:8000 truestate-backend
```

### Frontend Deployment

Automatically deployed to GitHub Pages on push to `main`:

1. Enable GitHub Pages in repository settings
2. Set source to "GitHub Actions"
3. Push to main branch
4. Visit: `https://yourusername.github.io/truestate`

Manual deployment:
```bash
cd frontend
npm run build
npm run deploy:ghpages
```

---

## Environment Variables

### Backend (.env)

```env
APP_ENV=production
DEBUG=false
API_HOST=0.0.0.0
API_PORT=8000
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/truestate
CACHE_BACKEND=redis
REDIS_URL=redis://host:6379/0
CORS_ORIGINS=https://yourusername.github.io
RATE_LIMIT_PER_MINUTE=60
LOG_LEVEL=INFO
```

### Frontend (.env)

```env
VITE_API_URL=https://your-backend-api.com
```

---

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_query_builder.py

# Verify no Pydantic warnings
python scripts/verify_no_pydantic_warnings.py
```

**Coverage**: > 85% target

### Frontend Tests

```bash
cd frontend

# Run all tests
npm run test

# Run with coverage
npm run test:coverage

# Run specific test file
npm run test -- SearchBar.test.tsx

# Watch mode
npm run test -- --watch
```

**Coverage**: > 80% target

---

## Performance

- **Search**: < 50ms for FTS queries on 10K+ records
- **Filters**: < 100ms with proper indexes
- **Pagination**: < 50ms with offset/limit
- **Cache Hit Rate**: > 70% for repeated queries
- **Frontend Bundle**: < 300KB gzipped
- **Lighthouse Score**: 95+ performance

---

## Security

- ✅ Input validation with Pydantic v2
- ✅ Parameterized SQL queries (no SQL injection)
- ✅ CORS restricted to known origins
- ✅ Rate limiting (60 requests/minute per IP)
- ✅ Security headers (CSP, X-Frame-Options, etc.)
- ✅ No secrets in code (environment variables)
- ✅ HTTPS enforced in production

---

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

**Code Standards**:
- Backend: Black, Ruff, isort
- Frontend: ESLint, Prettier
- Tests required for new features
- Type hints required (Python and TypeScript)

---

## License

MIT License - see LICENSE file for details

---

## Support

- **Documentation**: `/docs/architecture.md`
- **Issues**: GitHub Issues
- **Email**: support@truestate.com

---

## Acknowledgments

- FastAPI for the excellent Python web framework
- React team for the frontend library
- Tailwind CSS for utility-first styling
- SQLite FTS5 for powerful full-text search

---

**Built with ❤️ by the TruEstate Team**
