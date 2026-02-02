from src.resumeTailorService.prompt_builder import PromptBuilder
from src.resumeTailorService.openai_client import OpenAIClient


class TailorService:
    """Orchestrates the entire resume tailoring process"""

    @staticmethod
    async def tailor_resume_to_job(user_id: str, resume_text: str, job_description: str) -> str:
        """
        Main orchestrator function that handles the entire tailoring workflow
        
        Steps:
        1. Build tailored prompt
        2. Call OpenAI
        3. Return tailored response
        """
        # Build prompt
        prompt = PromptBuilder.build_tailor_prompt(user_id, resume_text, job_description)

        # Get response from OpenAI
        client = OpenAIClient()
        tailored_response = await client.tailor_resume(prompt)

        return tailored_response
