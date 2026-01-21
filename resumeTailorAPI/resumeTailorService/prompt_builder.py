class PromptBuilder:
    """Constructs prompts for OpenAI based on resume and job description"""

    @staticmethod
    def build_tailor_prompt(user_id: str, resume_text: str, job_description: str) -> str:
        """
        Build a simple prompt to test the flow
        """
        prompt = "Write me hello world in java."
        
        return prompt
