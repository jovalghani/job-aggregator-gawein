"""
Job Aggregator API - Main Application
FastAPI server for serving job listings
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from config import API_CONFIG, CORS_ORIGINS

# Initialize FastAPI app
app = FastAPI(
    title=API_CONFIG["title"],
    description=API_CONFIG["description"],
    version=API_CONFIG["version"],
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Models for API Response
class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    description: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    apply_url: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    jobs: List[JobResponse]
    total: int
    page: int
    per_page: int


# Sample data for testing (before database connection)
SAMPLE_JOBS = [
    {
        "id": 1,
        "title": "Senior Backend Developer",
        "company": "Tech Startup Indonesia",
        "location": "Jakarta, Indonesia",
        "description": "Kami mencari Senior Backend Developer dengan pengalaman Python/FastAPI...",
        "salary_min": 15000000,
        "salary_max": 25000000,
        "apply_url": "https://example.com/apply/1",
        "created_at": datetime.now(),
    },
    {
        "id": 2,
        "title": "Data Analyst",
        "company": "E-Commerce Giant",
        "location": "Remote",
        "description": "Posisi Data Analyst untuk tim analytics. SQL dan Python required...",
        "salary_min": 10000000,
        "salary_max": 18000000,
        "apply_url": "https://example.com/apply/2",
        "created_at": datetime.now(),
    },
    {
        "id": 3,
        "title": "Flutter Mobile Developer",
        "company": "Fintech Company",
        "location": "Bandung, Indonesia",
        "description": "Develop mobile apps menggunakan Flutter untuk iOS dan Android...",
        "salary_min": 12000000,
        "salary_max": 20000000,
        "apply_url": "https://example.com/apply/3",
        "created_at": datetime.now(),
    },
]


# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Job Aggregator API is running",
        "version": API_CONFIG["version"],
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "not_connected",  # Will update when DB is connected
    }


@app.get("/jobs", response_model=JobListResponse)
async def get_jobs(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    keyword: Optional[str] = Query(None, description="Search keyword"),
    location: Optional[str] = Query(None, description="Filter by location"),
    min_salary: Optional[int] = Query(None, description="Minimum salary filter"),
):
    """
    Get list of job postings with optional filters
    """
    # Filter jobs based on parameters
    filtered_jobs = SAMPLE_JOBS.copy()
    
    if keyword:
        keyword_lower = keyword.lower()
        filtered_jobs = [
            job for job in filtered_jobs
            if keyword_lower in job["title"].lower() 
            or keyword_lower in job["description"].lower()
        ]
    
    if location:
        location_lower = location.lower()
        filtered_jobs = [
            job for job in filtered_jobs
            if location_lower in job["location"].lower()
        ]
    
    if min_salary:
        filtered_jobs = [
            job for job in filtered_jobs
            if job.get("salary_min") and job["salary_min"] >= min_salary
        ]
    
    # Pagination
    total = len(filtered_jobs)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_jobs = filtered_jobs[start:end]
    
    return JobListResponse(
        jobs=[JobResponse(**job) for job in paginated_jobs],
        total=total,
        page=page,
        per_page=per_page,
    )


@app.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job_by_id(job_id: int):
    """Get a specific job by ID"""
    for job in SAMPLE_JOBS:
        if job["id"] == job_id:
            return JobResponse(**job)
    
    raise HTTPException(status_code=404, detail="Job not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
