"""
Job Aggregator - Job Scraper
Scrapes job listings and processes with Gemini AI
"""
import os
import json
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


class JobScraper:
    """
    Scraper untuk mengambil lowongan kerja dari berbagai sumber
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        
        # Initialize Gemini model
        if GEMINI_API_KEY:
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY not set. AI cleaning disabled.")
    
    def scrape_stackoverflow_rss(self) -> List[Dict]:
        """
        Scrape jobs from StackOverflow Jobs RSS feed (example source)
        Note: StackOverflow Jobs was discontinued, using this as example structure
        """
        # Using a sample RSS feed for demonstration
        # In production, replace with actual job board RSS/API
        sample_jobs = [
            {
                "title": "Python Developer",
                "company": "Tech Company A",
                "location": "Jakarta, Indonesia",
                "description": """
                    We are looking for a Python Developer to join our team.
                    Requirements:
                    - 3+ years experience with Python
                    - Experience with Django or FastAPI
                    - Knowledge of PostgreSQL
                    - Good communication skills
                    Salary: Competitive, based on experience
                    Remote work available.
                """,
                "apply_url": "https://example.com/jobs/python-dev",
            },
            {
                "title": "Senior Data Engineer",
                "company": "Analytics Corp",
                "location": "Remote",
                "description": """
                    Senior Data Engineer needed for building data pipelines.
                    Requirements:
                    - 5+ years in data engineering
                    - Expert in Apache Spark, Airflow
                    - Strong SQL skills
                    - Experience with cloud platforms (AWS/GCP)
                    Salary range: 25-35 juta/bulan
                    Full remote position.
                """,
                "apply_url": "https://example.com/jobs/data-engineer",
            },
        ]
        
        return sample_jobs
    
    def scrape_from_url(self, url: str) -> List[Dict]:
        """
        Generic scraper for job listing pages
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Generic job extraction (adjust selectors based on target site)
            jobs = []
            job_cards = soup.find_all('div', class_='job-card')  # Example selector
            
            for card in job_cards:
                title = card.find('h2', class_='title')
                company = card.find('span', class_='company')
                location = card.find('span', class_='location')
                description = card.find('div', class_='description')
                link = card.find('a', class_='apply')
                
                if title and link:
                    jobs.append({
                        "title": title.get_text(strip=True),
                        "company": company.get_text(strip=True) if company else "Unknown",
                        "location": location.get_text(strip=True) if location else "Unknown",
                        "description": description.get_text(strip=True) if description else "",
                        "apply_url": link.get('href', ''),
                    })
            
            return jobs
            
        except requests.RequestException as e:
            print(f"Error scraping {url}: {e}")
            return []
    
    def clean_with_ai(self, job_description: str) -> Dict[str, Any]:
        """
        Use Gemini AI to extract structured data from job description
        
        Args:
            job_description: Raw job description text
            
        Returns:
            Dict containing:
            - skills: list of required skills
            - experience_level: 'junior', 'mid', or 'senior'
            - is_remote: boolean indicating if remote work is available
        """
        if not self.model:
            # Return default values if AI is not available
            return {
                "skills": [],
                "experience_level": "unknown",
                "is_remote": False
            }
        
        prompt = f"""
Analyze the following job description and extract structured information.
Return ONLY a valid JSON object with these exact fields:
- "skills": an array of technical skills mentioned (programming languages, frameworks, tools)
- "experience_level": one of "junior" (0-2 years), "mid" (2-5 years), or "senior" (5+ years)
- "is_remote": true if remote work is mentioned, false otherwise

Job Description:
{job_description}

Return ONLY the JSON object, no other text.
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Clean up response (remove markdown code blocks if present)
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            result = json.loads(result_text.strip())
            
            # Validate and ensure correct types
            return {
                "skills": result.get("skills", []) if isinstance(result.get("skills"), list) else [],
                "experience_level": result.get("experience_level", "unknown"),
                "is_remote": bool(result.get("is_remote", False))
            }
            
        except json.JSONDecodeError as e:
            print(f"Error parsing AI response: {e}")
            return {
                "skills": [],
                "experience_level": "unknown",
                "is_remote": False
            }
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return {
                "skills": [],
                "experience_level": "unknown",
                "is_remote": False
            }
    
    def process_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """
        Process scraped jobs with AI to extract structured data
        """
        processed_jobs = []
        
        for job in jobs:
            print(f"Processing: {job['title']} at {job['company']}")
            
            # Extract AI insights
            ai_data = self.clean_with_ai(job.get('description', ''))
            
            # Merge AI data with job data
            processed_job = {
                **job,
                "skills": ai_data.get("skills", []),
                "experience_level": ai_data.get("experience_level", "unknown"),
                "is_remote": ai_data.get("is_remote", False),
                "scraped_at": datetime.utcnow().isoformat(),
            }
            
            processed_jobs.append(processed_job)
            
            # Rate limiting to avoid API limits
            time.sleep(1)
        
        return processed_jobs


def run_scraper():
    """
    Main function to run the job scraper
    """
    print("=" * 50)
    print("Job Aggregator - Scraper")
    print("=" * 50)
    
    scraper = JobScraper()
    
    # Scrape from sample source
    print("\n📡 Scraping jobs...")
    raw_jobs = scraper.scrape_stackoverflow_rss()
    print(f"Found {len(raw_jobs)} jobs")
    
    # Process with AI
    print("\n🤖 Processing with AI...")
    processed_jobs = scraper.process_jobs(raw_jobs)
    
    # Output results
    print("\n✅ Processed Jobs:")
    print("-" * 50)
    
    for job in processed_jobs:
        print(f"\n📌 {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Skills: {', '.join(job['skills']) if job['skills'] else 'N/A'}")
        print(f"   Level: {job['experience_level']}")
        print(f"   Remote: {'Yes' if job['is_remote'] else 'No'}")
    
    # Save to JSON file
    output_file = "scraped_jobs.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_jobs, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved to {output_file}")
    
    return processed_jobs


if __name__ == "__main__":
    run_scraper()
