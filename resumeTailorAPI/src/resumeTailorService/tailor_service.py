from src.resumeTailorService.prompt_builder import PromptBuilder
from src.resumeTailorService.openai_client import OpenAIClient
from src.models import Resume
from sqlalchemy.orm import Session


class TailorService:

    @staticmethod
    async def tailor_resume_to_job(resume_id: int, job_description: str, db: Session) -> str:
        resume = db.query(Resume).filter(Resume.resumeId == resume_id).first()
        if not resume:
            raise ValueError(f"Resume with id {resume_id} not found")

        prompt = PromptBuilder.build_tailor_prompt(resume.resumeText, job_description)
        client = OpenAIClient()
        tailored_response = await client.tailor_resume(prompt)

        return tailored_response
