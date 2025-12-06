"""Frontend README."""
# TruEstate Frontend

React + TypeScript frontend for the TruEstate Retail Sales Management System.

## Features

- Modern dark theme with glassmorphism UI
- Full-text search with debounced input
- Advanced filtering (8 filter types)
- Sorting (6 options)
- Pagination with metadata
- Responsive design
- React Query for data caching
- TypeScript strict mode

## Setup

```bash
npm install
npm run dev
```

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm test` - Run tests
- `npm run test:coverage` - Run tests with coverage
- `npm run lint` - Lint code
- `npm run deploy:ghpages` - Deploy to GitHub Pages

## Environment Variables

Create `.env` file:
```env
VITE_API_URL=http://localhost:8000
```

## Tech Stack

- React 18
- TypeScript 5
- Vite 5
- Tailwind CSS 3.4
- TanStack Query v5
- Axios
- Vitest

## Project Structure

```
src/
├── components/     # React components
├── hooks/          # Custom hooks
├── services/       # API client
├── types/          # TypeScript types
├── test/           # Tests
├── App.tsx         # Root component
├── main.tsx        # Entry point
└── index.css       # Global styles
```
