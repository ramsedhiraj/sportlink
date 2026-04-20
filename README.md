# SportLink - AI-Powered Athlete Discovery Platform

Public repository for SportLink application.

## Features

- JWT Authentication with role-based access
- User profiles (Athlete, NGO, Coach, Admin)
- Social feed with posts, likes, comments
- AI recommendation engine
- Dynamic ranking system
- NGO athlete support system
- Real-time WebSocket chat
- Real-time notifications

## Quick Start

### Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload

### Frontend
cd frontend
npm install
npm run dev

## Tech Stack

- Backend: FastAPI + PostgreSQL + SQLAlchemy
- Frontend: React 18 + Vite + Tailwind CSS
- Real-time: WebSockets
- AI: scikit-learn

## Setup Guide

See SETUP.md for detailed instructions.

## License

MIT License