from fastapi import HTTPException


class DataProcessor:
    """Handles validation and formatting of resume and job description data"""

    @staticmethod
    def validate_resume_text(resume_text: str) -> str:
        """Validate and clean resume text"""
        if not resume_text or len(resume_text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Resume text cannot be empty")
        
        return resume_text.strip()

    @staticmethod
    def validate_job_description(job_description: str) -> str:
        """Validate and clean job description text"""
        if not job_description or len(job_description.strip()) == 0:
            raise HTTPException(status_code=400, detail="Job description cannot be empty")
        
        return job_description.strip()
