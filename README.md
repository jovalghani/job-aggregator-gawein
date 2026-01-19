# Job Aggregator

Full-stack job aggregator application dengan Python Backend, AI Scraper, dan Flutter Mobile App.

## Project Structure

```
├── backend/          # FastAPI Backend Server
├── scraper/          # AI-Powered Job Scraper  
└── mobile-app/       # Flutter Android App
```

## Quick Start

### 1. Backend API

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API Docs: http://localhost:8000/docs

> **Note**: Secara default, API menggunakan **Mock Data** (sample data) untuk kemudahan testing.
> Untuk menggunakan database PostgreSQL:
> 1. Setup PostgreSQL database
> 2. Update `.env` dengan credentials database
> 3. Update `main.py` untuk menggunakan `get_db` dependency


### 2. Job Scraper

```bash
cd scraper
pip install -r requirements.txt
# Set GEMINI_API_KEY di .env
python job_scraper.py
```

### 3. Mobile App

```bash
cd mobile-app
flutter pub get
flutter run
```

## Configuration

Edit file `.env` di folder `backend/` dan `scraper/` dengan credentials yang sesuai.

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **AI**: Google Gemini API
- **Mobile**: Flutter, Provider, Material 3
