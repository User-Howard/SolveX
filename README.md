# SolveX

> A Knowledge Management Platform for Programming Learning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

SolveX is a knowledge management system for programming learners that centralizes learning resources from different platforms (Stack Overflow, documentation, blogs, etc.). It helps organize problems, solutions, and resources in one place, making the learning process more efficient.

### Key Features

- **Problem Management**: Create, track, and manage programming problems
- **Solution Recording**: Store and organize multiple solution approaches
- **Resource Integration**: Aggregate external learning resources and reference links
- **Tagging System**: Categorize and search knowledge using tags
- **Version Tracking**: Record solution evolution and improvement history
- **Dashboard**: Visualize learning statistics and progress

## Tech Stack

### Backend

- **Framework**: FastAPI
- **Language**: Python 3.12+
- **Database**: PostgreSQL 16
- **API Documentation**: Auto-generated OpenAPI (Swagger)
- **Package Manager**: uv

### Frontend

- **Framework**: Next.js 16 (App Router)
- **UI Library**: React 19
- **Styling**: Tailwind CSS 4 + DaisyUI 5
- **Language**: TypeScript
- **Features**: Responsive design, dark mode support

### Containerization

- **Docker Compose**: Unified management of frontend, backend, and database services

## Quick Start

### Prerequisites

- Docker & Docker Compose
- (Optional) Node.js 18+ and Python 3.12+ for local development

### Using Docker Compose (Recommended)

```bash
# Start all services
docker compose up

# Run in background
docker compose up -d
```

Services will be available at:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development

#### Backend

```bash
cd backend

# Install dependencies
uv sync

# Set up environment variables
cp .env.development .env

# Start development server
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Project Structure

```
SolveX/
├── backend/              # FastAPI backend
│   ├── src/
│   │   ├── api/         # API routes and services
│   │   │   ├── routes/  # Route definitions
│   │   │   ├── schemas/ # Pydantic models
│   │   │   └── services/# Business logic
│   │   ├── db/          # Database connection and initialization
│   │   ├── config.py    # Configuration management
│   │   └── main.py      # Application entry point
│   ├── Dockerfile
│   └── pyproject.toml
│
├── frontend/            # Next.js frontend
│   ├── app/            # Next.js App Router pages
│   │   ├── problems/   # Problem-related pages
│   │   └── resources/  # Resource pages
│   ├── components/     # React components
│   ├── lib/            # Utility functions and API client
│   ├── types/          # TypeScript type definitions
│   └── Dockerfile
│
├── docs/               # Project documentation
├── report/             # Project report (Typst)
├── compose.yml         # Docker Compose configuration
├── Makefile            # Cleanup commands
└── README.md
```

## API Endpoints

Main API endpoints include:

- `GET /api/v1/problems` - Get problem list
- `POST /api/v1/problems` - Create new problem
- `GET /api/v1/problems/{id}` - Get problem details
- `GET /api/v1/solutions` - Get solution list
- `POST /api/v1/solutions` - Create new solution
- `GET /api/v1/resources` - Get resource list
- `GET /api/v1/tags` - Get tag list
- `GET /api/v1/dashboard` - Get dashboard statistics

Full API documentation available at: http://localhost:8000/docs

## Database Schema

The project uses a relational database design with the following main entities:

- **Users**: User data
- **Problems**: Programming problems
- **Solutions**: Solution approaches
- **Resources**: External resources
- **Tags**: Tag categories

Key relationships:

- `creates`: Users create problems/solutions
- `has_solutions`: Problems have multiple solutions
- `has_tags`: Problems/solutions have multiple tags
- `refer`: Solutions reference external resources
- `evolve_from`: Solution version evolution

See `report/assets/er-diagram.svg` for the detailed ER diagram.

## Development Commands

```bash
# Clean project (remove cache, node_modules, etc.)
make clean

# Stop all containers
docker compose down

# Stop and remove all data
docker compose down -v

# View container logs
docker compose logs -f

# Rebuild containers
docker compose up --build
```

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/solvex
LOAD_FAKE_DATA=true
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Background

This is a final project for Database Systems course that addresses the problem of fragmented learning resources. As programming learners ourselves, we experienced the frustration of searching across multiple platforms, so we built SolveX to centralize and organize this information.

## License

This project is licensed under the [MIT License](LICENSE).

### Font Licenses

This project uses the following fonts in the report:

- **[JetBrains Mono](https://github.com/JetBrains/JetBrainsMono)** - Licensed under [SIL Open Font License 1.1](https://github.com/JetBrains/JetBrainsMono/blob/master/OFL.txt)
- **[Noto Sans TC](https://fonts.google.com/noto/specimen/Noto+Sans+TC)** - Licensed under [SIL Open Font License 1.1](http://scripts.sil.org/OFL)

## Team

**Team 33** - Database Systems Final Project
