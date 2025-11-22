"""
API Handler - Entry point for processing job requests
This is where the backend receives the JSON request from the frontend
"""
import json
from job_processor import process_job_request


def handle_job_request(json_data):
    """
    Entry point: Receives JSON object with all job data
    This would be called from your API endpoint (Flask/FastAPI/etc.)
    
    Expected JSON structure:
    {
        "user_id": "uuid-string",
        "resume_id": "uuid-string",
        "title": "Software Engineer",
        "company_name": "Tech Corp",
        "job_description": "We are looking for..."
    }
    
    Returns:
        dict: The completed job with tailored resume
    """
    try:
        # Parse JSON (if it's a string, otherwise assume it's already a dict)
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
        
        # Extract required fields
        user_id = data.get('user_id')
        resume_id = data.get('resume_id')
        title = data.get('title')
        company_name = data.get('company_name')
        job_description = data.get('job_description')
        
        # Validate required fields
        if not user_id:
            raise ValueError("user_id is required")
        if not job_description:
            raise ValueError("job_description is required")
        
        print(f"📥 Received job request:")
        print(f"   User ID: {user_id}")
        print(f"   Resume ID: {resume_id}")
        print(f"   Title: {title}")
        print(f"   Company: {company_name}")
        
        # Process the job request
        result = process_job_request(
            user_id=user_id,
            resume_id=resume_id,
            title=title,
            company_name=company_name,
            job_description=job_description
        )
        
        return result
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
    except Exception as e:
        raise Exception(f"Error processing job request: {e}")


# Example usage
if __name__ == "__main__":
    # Example JSON request (simulating what frontend would send)
    example_request = {
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "resume_id": "660e8400-e29b-41d4-a716-446655440000",
        "title": "Senior Software Engineer",
        "company_name": "Tech Corp",
        "job_description": "We are looking for a Senior Software Engineer with 5+ years of experience in Python, JavaScript, and cloud technologies."
    }
    
    print("=" * 60)
    print("Example: Processing Job Request from JSON")
    print("=" * 60)
    print(f"\n📥 JSON Request:\n{json.dumps(example_request, indent=2)}\n")
    
    # In real usage, this would be called from your API endpoint
    # result = handle_job_request(example_request)
    # print(f"\n✅ Result:\n{json.dumps(result, indent=2, default=str)}")

