# TruEstate Architecture Documentation

## System Overview

TruEstate is a modern retail sales management system built with a decoupled architecture:
- **Backend**: FastAPI (Python 3.11+) REST API with SQLite/PostgreSQL
- **Frontend**: React + TypeScript + Tailwind CSS SPA
- **Deployment**: Backend on cloud platforms, Frontend on GitHub Pages

## Backend Architecture

### Technology Stack

- **Framework**: FastAPI 0.109+
- **Language**: Python 3.11+
- **Database**: SQLite (FTS5) for development, PostgreSQL for production
- **ORM**: SQLAlchemy 2.0 (async)
- **Validation**: Pydantic v2
- **Caching**: In-memory (cachetools) or Redis
- **Testing**: pytest, pytest-asyncio

### Layer Architecture

```
┌─────────────────────────────────────┐
│         FastAPI Application          │
│  (Middleware, CORS, Rate Limiting)   │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│           Routes Layer               │
│  (transactions.py, meta.py)          │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│          Services Layer              │
│  (TransactionService, QueryBuilder)  │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│          Models Layer                │
│  (SQLAlchemy Models, Schemas)        │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│         Database Layer               │
│  (SQLite FTS5 / PostgreSQL)          │
└─────────────────────────────────────┘
```

### Module Responsibilities

#### Routes (`src/routes/`)
- **transactions.py**: Transaction CRUD endpoints with search, filter, sort, pagination
- **meta.py**: Filter metadata and health check endpoints
- Responsibility: HTTP request handling, validation, response formatting

#### Services (`src/services/`)
- **TransactionService**: Business logic for transactions
- **QueryBuilder**: Complex query construction with search, filters, sorting
- Responsibility: Business logic, caching, query composition

#### Models (`src/models/`)
- **transaction.py**: SQLAlchemy Transaction model with indexes
- **base.py**: Base model classes and database session management
- Responsibility: Data modeling, database schema, ORM mappings

#### Schemas (`src/schemas/`)
- **transaction.py**: Pydantic models for request/response validation
- Responsibility: Input validation, serialization, type safety

#### Utils (`src/utils/`)
- **cache.py**: Pluggable caching layer (memory/Redis)
- **logging.py**: Structured JSON logging
- Responsibility: Cross-cutting concerns

#### Middleware (`src/middleware.py`)
- **RequestIDMiddleware**: Request tracking with unique IDs
- **RateLimitMiddleware**: Simple per-IP rate limiting
- **SecurityHeadersMiddleware**: Security headers and ETag support

### Full-Text Search Implementation

#### SQLite FTS5 (Development)
```sql
CREATE VIRTUAL TABLE transactions_fts USING fts5(
    customer_name,
    phone_number,
    content='transactions',
    content_rowid='id'
);
```

**Query Flow**:
1. User enters search term → normalized (lowercase, strip)
2. Query FTS virtual table with MATCH operator
3. Join results with main transactions table
4. Apply additional filters and sorting
5. Return paginated results

**Advantages**:
- No external dependencies
- Fast full-text search
- Cross-platform compatibility

#### PostgreSQL (Production Alternative)
```sql
CREATE INDEX idx_transactions_fts ON transactions 
USING GIN(to_tsvector('english', customer_name || ' ' || phone_number));
```

Uses `pg_trgm` for fuzzy matching and `tsvector` for full-text search.

### Filter Implementation

**Multi-Select Filters**:
- Region, Gender, Category, Tags, Payment Method
- SQL: `WHERE field IN (value1, value2, ...)`
- Combined with AND logic between different filter types

**Range Filters**:
- Age: `WHERE age >= min AND age <= max`
- Date: `WHERE date >= from AND date <= to`

**Query Optimization**:
- Indexes on all filterable columns
- Composite indexes for common filter combinations
- Query builder creates optimal WHERE clauses

### Sorting Implementation

Supported sorts:
- Date: `ORDER BY date DESC/ASC`
- Quantity: `ORDER BY quantity DESC/ASC`
- Customer Name: `ORDER BY customer_name ASC/DESC`

**With Search**: When search query present, can order by relevance score or explicit sort parameter.

### Pagination Implementation

**Offset-based** (default):
```python
LIMIT = 10  # configurable, max 100
OFFSET = (page - 1) * LIMIT
```

Returns metadata:
```json
{
  "total": 500,
  "page": 1,
  "limit": 10,
  "total_pages": 50,
  "has_next": true,
  "has_prev": false
}
```

**Cursor-based** (optional for large datasets):
Uses keyset pagination with date+id composite key for stable ordering.

### Caching Strategy

**Cache Key Generation**:
```python
MD5(sorted_params_json) → "transactions_list:a1b2c3d4..."
```

**TTL**: 30 seconds (configurable)

**Backends**:
1. **Memory** (default): LRU + TTL cache using cachetools
2. **Redis** (production): Distributed cache for multi-instance deployments

**Cache Invalidation**:
- On data mutation (POST/PUT/DELETE)
- Manual clear via admin endpoint
- TTL expiration

**HTTP-level**:
- ETag: Hash of response body
- Cache-Control: `public, max-age=30`
- Supports conditional GET (304 Not Modified)

---

## Frontend Architecture

### Technology Stack

- **Framework**: React 18
- **Language**: TypeScript 5
- **Build Tool**: Vite 5
- **Styling**: Tailwind CSS 3.4
- **Data Fetching**: TanStack Query (React Query) v5
- **HTTP Client**: Axios
- **Testing**: Vitest, Testing Library

### Component Architecture

```
App (React Query Provider)
├── Header
├── TransactionsPage
│   ├── FilterPanel (sidebar)
│   │   ├── Multi-select checkboxes
│   │   └── Range inputs
│   ├── SearchBar (debounced)
│   ├── SortSelector
│   ├── AppliedFilters (chips)
│   ├── TransactionTable
│   │   └── TransactionRow × N
│   └── Pagination
└── Footer
```

### Module Responsibilities

#### Components (`src/components/`)
- **Header.tsx**: Top navigation and branding
- **SearchBar.tsx**: Debounced search input (300ms)
- **SortSelector.tsx**: Dropdown for sort options
- **FilterPanel.tsx**: Sidebar with all filters
- **AppliedFilters.tsx**: Removable filter chips
- **TransactionTable.tsx**: Responsive data table
- **Pagination.tsx**: Page navigation controls

#### Services (`src/services/`)
- **api.ts**: Axios client with interceptors
  - Request ID generation
  - Error handling
  - Query string building

#### Hooks (`src/hooks/`)
- **useApi.ts**: React Query hooks
  - `useTransactions`: Fetch transaction list
  - `useFilterMetadata`: Fetch filter options
  - `useTransaction`: Fetch single transaction

#### Types (`src/types/`)
- **api.ts**: TypeScript interfaces for API contracts

### State Management

**URL as State**: 
- All filters, search, sort, page stored in component state
- Can be easily synced to URL params for sharing/bookmarking

**React Query Cache**:
- Query key: `['transactions', filters]`
- Stale time: 30 seconds
- Cache time: 5 minutes
- Automatic background refetching on window focus

### Client-Side Caching

**Query Deduplication**: React Query prevents duplicate requests for same query key.

**Optimistic Updates**: Mutations can update cache optimistically before server confirmation.

**Pagination Prefetching**: Next page can be prefetched in background.

---

## Data Flow

### Read Flow (List Transactions)

```
User → SearchBar/Filters → State Update → React Query
  → API Request → Backend QueryBuilder → Database FTS + Filters
    → Results → Cache → Response → React Query Cache
      → Component Re-render → UI Update
```

### Write Flow (Create Transaction)

```
User → Form Submit → API Request → Backend Service
  → Database Insert → FTS Table Update → Cache Invalidation
    → Response → React Query Cache Invalidation
      → Refetch → UI Update
```

---

## Folder Structure

```
TueEstate/
├── backend/
│   ├── src/
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── routes/         # API endpoints
│   │   ├── utils/          # Utilities (cache, logging)
│   │   ├── middleware.py   # Middleware
│   │   ├── config.py       # Configuration
│   │   └── index.py        # FastAPI app
│   ├── scripts/
│   │   ├── seed_db.py                      # Database seeding
│   │   └── verify_no_pydantic_warnings.py  # Verification
│   ├── tests/              # pytest tests
│   ├── requirements.txt    # Python dependencies
│   ├── pyproject.toml      # Project config
│   ├── Dockerfile          # Container image
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API client
│   │   ├── types/          # TypeScript types
│   │   ├── test/           # Vitest tests
│   │   ├── App.tsx         # Root component
│   │   ├── main.tsx        # Entry point
│   │   └── index.css       # Global styles
│   ├── public/             # Static assets
│   ├── package.json        # Node dependencies
│   ├── vite.config.ts      # Vite config
│   ├── tailwind.config.js  # Tailwind config
│   └── tsconfig.json       # TypeScript config
├── docs/
│   └── architecture.md     # This file
├── .github/
│   └── workflows/          # CI/CD pipelines
├── .devcontainer/          # VS Code devcontainer
├── docker-compose.yml      # Docker orchestration
├── Makefile                # Build automation
├── run.ps1                 # Windows helper script
└── README.md               # Project README
```

---

## Security Considerations

1. **Input Validation**: Pydantic v2 strict validation on all inputs
2. **SQL Injection**: Parameterized queries throughout
3. **CORS**: Restricted to specified origins
4. **Rate Limiting**: Per-IP request throttling
5. **Security Headers**: CSP, X-Frame-Options, etc.
6. **Secrets**: Environment variables, never committed
7. **HTTPS**: Enforced in production

---

## Performance Optimizations

1. **Database Indexes**: All filterable and sortable columns
2. **FTS5 Virtual Table**: Fast full-text search
3. **Connection Pooling**: Async SQLAlchemy sessions
4. **Response Caching**: 30s TTL with ETag support
5. **Query Optimization**: Single query for list + count
6. **Frontend Code Splitting**: Vite dynamic imports
7. **CDN Deployment**: Static assets on GitHub Pages

---

## Scalability Path

### Horizontal Scaling
1. Multiple backend instances behind load balancer
2. Shared Redis cache for session/query cache
3. Read replicas for database (if PostgreSQL)

### Vertical Scaling
1. Increase database resources (CPU, RAM)
2. Tune SQLite page size and cache
3. Increase Redis memory

### Monitoring
1. Structured logging to centralized service (e.g., Datadog, CloudWatch)
2. Prometheus metrics endpoint for observability
3. APM for request tracing (e.g., New Relic, Sentry)

---

## Development Workflow

1. **Local Development**: `make dev-backend` + `make dev-frontend`
2. **Testing**: `make test` runs all tests with coverage
3. **Linting**: `make lint` checks code quality
4. **Docker**: `make docker-up` for full stack
5. **CI/CD**: GitHub Actions on push/PR
6. **Deployment**: Auto-deploy frontend to GH Pages on main branch push

---

## Production Deployment

### Backend Options
1. **Render**: One-click deploy, free tier available
2. **Railway**: Free tier, auto-deploy from GitHub
3. **Fly.io**: Global edge deployment
4. **Heroku**: Classic PaaS

### Frontend
- **GitHub Pages**: Automatic deployment via Actions
- URL: `https://<username>.github.io/<repo>/`

### Environment Variables
Set in platform dashboard:
- `DATABASE_URL` (PostgreSQL)
- `REDIS_URL`
- `CORS_ORIGINS` (include frontend URL)
- `API_PORT=8000`

---

## Future Enhancements

1. **Authentication**: JWT-based auth with role-based access
2. **Real-time**: WebSocket support for live updates
3. **Export**: CSV/Excel export functionality
4. **Advanced Analytics**: Charts and dashboards
5. **Audit Log**: Track all data changes
6. **Multi-tenancy**: Support multiple organizations
