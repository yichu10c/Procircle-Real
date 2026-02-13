from fastapi import HTTPException
from src.resumeTailorService.prompt_builder import PromptBuilder
from src.resumeTailorService.openai_client import OpenAIClient
from src.models import Resume
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class TailorService:

    @staticmethod
    async def tailor_resume_to_job(resume_id: int, job_description: str, db: Session) -> str:
        try:
            resume = db.query(Resume).filter(Resume.resumeId == resume_id).first()
            if not resume:
                raise HTTPException(status_code=404, detail=f"Resume with id {resume_id} not found")

            prompt = PromptBuilder.build_tailor_prompt(resume.resumeText, job_description)
            client = OpenAIClient()
            tailored_response = await client.tailor_resume(prompt)

            return tailored_response
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to tailor resume: {str(e)}")
