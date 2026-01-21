from resumeTailorService.data_processor import DataProcessor
from resumeTailorService.prompt_builder import PromptBuilder
from resumeTailorService.openai_client import OpenAIClient


class TailorService:
    """Orchestrates the entire resume tailoring process"""

    @staticmethod
    async def tailor_resume_to_job(user_id: str, resume_text: str, job_description: str) -> str:
        """
        Main orchestrator function that handles the entire tailoring workflow
        
        Steps:
        1. Validate resume and job description
        2. Build tailored prompt
        3. Call OpenAI
        4. Return tailored response
        """
        # Validate inputs
        validated_resume = DataProcessor.validate_resume_text(resume_text)
        validated_job = DataProcessor.validate_job_description(job_description)
        
        # Build prompt
        prompt = PromptBuilder.build_tailor_prompt(user_id, validated_resume, validated_job)

        # Get response from OpenAI
        client = OpenAIClient()
        tailored_response = await client.tailor_resume(prompt)

        return tailored_response
