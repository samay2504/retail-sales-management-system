# Quick Start Guide

## Windows Users

```powershell
# 1. Install Python 3.11+ and Node.js 20+

# 2. Open PowerShell in project directory
cd D:\Projects2.0\TueEstate

# 3. Run setup
.\run.ps1 setup
.\run.ps1 install
.\run.ps1 seed

# 4. Start backend (Terminal 1)
.\run.ps1 dev-backend

# 5. Start frontend (Terminal 2)
.\run.ps1 dev-frontend

# 6. Visit http://localhost:5173
```

## macOS / Linux Users

```bash
# 1. Install Python 3.11+ and Node.js 20+

# 2. Open terminal in project directory
cd ~/Projects/TueEstate

# 3. Run setup
make setup
make install
make seed

# 4. Start backend (Terminal 1)
make dev-backend

# 5. Start frontend (Terminal 2)
make dev-frontend

# 6. Visit http://localhost:5173
```

## Docker Users

```bash
# Start everything with Docker
docker-compose up -d

# View logs
docker-compose logs -f

# Backend: http://localhost:8000
# Frontend: Install and run separately (see above)
```

## Troubleshooting

### "Python not found"
Install Python 3.11+ from python.org

### "Node not found"
Install Node.js 20+ from nodejs.org

### "Permission denied"
Windows: Run PowerShell as Administrator
Unix: Use `sudo` if needed

### "Module not found"
Backend: `cd backend && pip install -r requirements.txt`
Frontend: `cd frontend && npm install`

### "Database locked"
Stop any running instances: `pkill -f uvicorn` (Unix) or Task Manager (Windows)

## Next Steps

1. Explore the API: http://localhost:8000/api/docs
2. Test search and filters in the frontend
3. Run tests: `.\run.ps1 test` or `make test`
4. Read the full README.md for deployment instructions
