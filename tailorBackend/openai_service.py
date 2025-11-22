"""
OpenAI Service - Handles prompt creation and API calls
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def create_tailoring_prompt(job_data):
    """
    Step 4: Create a prompt for OpenAI based on job data
    
    Args:
        job_data: Dictionary containing user, resume, job_description, etc.
    
    Returns:
        str: The formatted prompt for OpenAI
    """
    resume_text = job_data['resume']['parsed_text'] if job_data['resume'] and job_data['resume']['parsed_text'] else "No resume provided"
    job_description = job_data['job_description']
    title = job_data.get('title', 'this position')
    company_name = job_data.get('company_name', 'the company')
    
    prompt = f"""You are a professional resume tailoring expert. Your task is to tailor a resume for a specific job application.

JOB INFORMATION:
- Position: {title}
- Company: {company_name}

JOB DESCRIPTION:
{job_description}

ORIGINAL RESUME:
{resume_text}

INSTRUCTIONS:
1. Analyze the job description and identify key requirements, skills, and qualifications
2. Review the original resume and identify relevant experience, skills, and achievements
3. Tailor the resume to highlight the most relevant qualifications for this specific position
4. Maintain the original structure and format of the resume
5. Emphasize relevant keywords from the job description
6. Reorder or emphasize sections as needed to showcase the best fit
7. Keep all truthful information - do not add false information
8. Return the complete tailored resume as your response

Please provide the tailored resume that best matches this job opportunity:"""
    
    return prompt


def call_openai_api(prompt, model="gpt-4-turbo-preview", temperature=0.7):
    """
    Step 5: Call OpenAI API with the prompt
    
    Args:
        prompt: The prompt string to send to OpenAI
        model: OpenAI model to use (default: gpt-4-turbo-preview)
        temperature: Temperature setting for the model (default: 0.7)
    
    Returns:
        str: The tailored resume text from OpenAI
    """
    # Get API key from environment
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    try:
        # Make API call
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional resume tailoring expert. You help job seekers customize their resumes for specific job applications."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=4000  # Adjust based on your needs
        )
        
        # Extract the tailored resume from the response
        tailored_resume = response.choices[0].message.content.strip()
        
        # Optional: Log token usage
        if hasattr(response, 'usage'):
            print(f"   Tokens used: {response.usage.total_tokens}")
            print(f"   Prompt tokens: {response.usage.prompt_tokens}")
            print(f"   Completion tokens: {response.usage.completion_tokens}")
        
        return tailored_resume
        
    except Exception as e:
        raise Exception(f"OpenAI API error: {e}")


def test_openai_connection():
    """
    Test function to verify OpenAI API connection
    """
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ OPENAI_API_KEY not found in environment")
            return False
        
        client = OpenAI(api_key=api_key)
        
        # Simple test call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello' if you can read this."}],
            max_tokens=10
        )
        
        print("✅ OpenAI API connection successful")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API connection failed: {e}")
        return False


if __name__ == "__main__":
    # Test OpenAI connection
    print("Testing OpenAI connection...")
    test_openai_connection()

