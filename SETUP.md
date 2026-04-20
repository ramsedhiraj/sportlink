# Setup Guide for Windows

## Prerequisites

- Python 3.11+ (from python.org)
- Node.js 18+ (from nodejs.org)
- PostgreSQL 14+ (from postgresql.org)
- Git

## Backend Setup

1. Open PowerShell
2. cd backend
3. python -m venv venv
4. venv\Scripts\activate
5. pip install -r requirements.txt
6. copy .env.example .env
7. Edit .env with your database credentials
8. uvicorn app.main:app --reload

Backend runs on: http://localhost:8000
API Docs: http://localhost:8000/docs

## Frontend Setup

1. Open new PowerShell
2. cd frontend
3. npm install
4. npm run dev

Frontend runs on: http://localhost:5173

## Database

PostgreSQL connection string in .env:
DATABASE_URL=postgresql://user:password@localhost:5432/sportlink_db

## Create Test Account

1. Visit http://localhost:5173
2. Click Register
3. Fill form and create account
4. Login and start using

## Docker (Optional)

docker-compose up --build

Services:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Database: localhost:5432