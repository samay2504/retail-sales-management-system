"""Backend README."""
# TruEstate Backend

FastAPI backend for the TruEstate Retail Sales Management System.

## Features

- **Full-text Search**: SQLite FTS5 for fast customer name and phone number search
- **Advanced Filtering**: Multi-select and range filters for all transaction attributes
- **Sorting**: Support for date, quantity, and customer name sorting
- **Pagination**: Efficient offset-based pagination with metadata
- **Caching**: Pluggable caching layer (in-memory or Redis)
- **Rate Limiting**: Built-in rate limiting middleware
- **Security**: CORS, security headers, and input validation
- **Structured Logging**: JSON logging with request tracking

## Setup

### Prerequisites

- Python 3.11+
- pip or poetry

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Seed the database:
```bash
python scripts/seed_db.py 500
```

4. Run the server:
```bash
uvicorn src.index:app --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation

Interactive API docs: `http://localhost:8000/api/docs`

## Testing

Run tests:
```bash
pytest
```

With coverage:
```bash
pytest --cov=src --cov-report=html
```

## Environment Variables

See `.env.example` for all available configuration options.
