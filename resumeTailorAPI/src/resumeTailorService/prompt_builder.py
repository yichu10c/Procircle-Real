class PromptBuilder:
    """Constructs prompts for OpenAI based on resume and job description"""

    @staticmethod
    def build_tailor_prompt(user_id: str, resume_text: str, job_description: str) -> str:
        """
        Build a prompt to extract all skills from the resume
        """
        prompt = f"""Extract and list ALL skills from the following resume. 
        
        Resume:
        {resume_text}
        
        Please provide a comprehensive list of all technical, soft, and professional skills mentioned in the resume."""
        
        return prompt
