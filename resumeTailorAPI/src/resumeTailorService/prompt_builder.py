class PromptBuilder:

    @staticmethod
    def build_tailor_prompt(resume_text: str, job_description: str) -> str:
        prompt = f"""Extract and list ALL skills from the following resume.

Resume:
{resume_text}

Then, compare those skills against the following job description and identify which skills are relevant.

Job Description:
{job_description}

Please provide a comprehensive list of all technical, soft, and professional skills mentioned in the resume."""

        return prompt
