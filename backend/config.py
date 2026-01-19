"""
Job Aggregator API - Configuration
Database connection settings for PostgreSQL (Supabase)
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration (Replace with your Supabase credentials)
DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "db.xxxxxxxxxxxxx.supabase.co"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "your-secure-password"),
}

# Construct Database URL
DATABASE_URL = (
    f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}"
    f"@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
)

# API Configuration
API_CONFIG = {
    "title": "Job Aggregator API",
    "description": "API untuk mengumpulkan dan menyajikan lowongan kerja",
    "version": "1.0.0",
}

# CORS Settings
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
