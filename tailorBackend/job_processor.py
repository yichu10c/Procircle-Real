"""
Job Processing Service
Handles the complete workflow for processing a job tailoring request
"""
from job import create_job, get_job_by_id, complete_job, mark_job_as_failed, update_job
from resume import get_resume_by_id
from user import get_user_by_id
from openai_service import create_tailoring_prompt, call_openai_api
import os


def process_job_request(user_id, resume_id=None, title=None, company_name=None, job_description=None):
    """
    Main workflow function - processes a job request from start to finish
    
    Flow:
    1. Validate input
    2. Create job record in database (status: PENDING)
    3. Prepare data for OpenAI
    4. Create prompts
    5. Call OpenAI API
    6. Store tailored resume in database (status: COMPLETED)
    
    Args:
        user_id: User ID (required)
        resume_id: Resume ID (optional)
        title: Job title (optional)
        company_name: Company name (optional)
        job_description: Job description (required)
    
    Returns:
        dict: The completed job with tailored resume
    """
    job_id = None
    
    try:
        # ============================================
        # STEP 1: Validate the request
        # ============================================
        print("\n" + "=" * 60)
        print("STEP 1: Validating Request")
        print("=" * 60)
        validate_job_request(user_id, resume_id, job_description)
        print("✅ Validation passed")
        
        # ============================================
        # STEP 2: Create job record in database
        # ============================================
        print("\n" + "=" * 60)
        print("STEP 2: Creating Job Record in Database")
        print("=" * 60)
        
        job = create_job(
            user_id=user_id,
            resume_id=resume_id,
            title=title,
            company_name=company_name,
            job_description=job_description,
            status='PENDING'  # Job is not complete yet
        )
        
        job_id = job['id']
        print(f"✅ Job created in database")
        print(f"   Job ID: {job_id}")
        print(f"   Status: {job['status']}")
        print(f"   Note: Job is incomplete - tailored_resume_text is NULL")
        
        # ============================================
        # STEP 3: Prepare data for OpenAI
        # ============================================
        print("\n" + "=" * 60)
        print("STEP 3: Preparing Data for OpenAI")
        print("=" * 60)
        
        job_data = prepare_job_data(user_id, resume_id, job_description, title, company_name)
        print("✅ Data prepared")
        print(f"   Resume text length: {len(job_data['resume']['parsed_text']) if job_data['resume'] else 0} chars")
        print(f"   Job description length: {len(job_description)} chars")
        
        # ============================================
        # STEP 4: Create prompts for OpenAI
        # ============================================
        print("\n" + "=" * 60)
        print("STEP 4: Creating Prompts for OpenAI")
        print("=" * 60)
        
        prompt = create_tailoring_prompt(job_data)
        print("✅ Prompt created")
        print(f"   Prompt length: {len(prompt)} chars")
        
        # ============================================
        # STEP 5: Call OpenAI API
        # ============================================
        print("\n" + "=" * 60)
        print("STEP 5: Calling OpenAI API")
        print("=" * 60)
        
        print("   Sending request to OpenAI...")
        tailored_resume = call_openai_api(prompt)
        print("✅ Received response from OpenAI")
        print(f"   Tailored resume length: {len(tailored_resume)} chars")
        
        # ============================================
        # STEP 6: Store tailored resume in database
        # ============================================
        print("\n" + "=" * 60)
        print("STEP 6: Storing Tailored Resume in Database")
        print("=" * 60)
        
        completed_job = complete_job(job_id, tailored_resume)
        print("✅ Job completed and saved to database")
        print(f"   Job ID: {completed_job['id']}")
        print(f"   Status: {completed_job['status']}")
        print(f"   Tailored resume stored: ✅")
        
        print("\n" + "=" * 60)
        print("✅ WORKFLOW COMPLETE")
        print("=" * 60)
        
        return completed_job
        
    except ValueError as e:
        # Validation errors
        print(f"\n❌ Validation error: {e}")
        raise
    except Exception as e:
        # Processing errors - mark job as failed
        print(f"\n❌ Processing error: {e}")
        if job_id:
            try:
                mark_job_as_failed(job_id)
                print(f"⚠️  Job {job_id} marked as FAILED")
            except:
                pass
        raise


def validate_job_request(user_id, resume_id=None, job_description=None):
    """
    Step 1: Validate the incoming job request
    """
    errors = []
    
    # Validate user exists
    user = get_user_by_id(user_id)
    if not user:
        errors.append(f"User with ID {user_id} not found")
    
    # Validate resume exists if provided
    if resume_id:
        resume = get_resume_by_id(resume_id)
        if not resume:
            errors.append(f"Resume with ID {resume_id} not found")
        elif resume['user_id'] != user_id:
            errors.append("Resume does not belong to the specified user")
    
    # Validate job description is provided
    if not job_description or not job_description.strip():
        errors.append("Job description is required")
    
    if errors:
        raise ValueError("Validation failed: " + "; ".join(errors))
    
    return True


def prepare_job_data(user_id, resume_id=None, job_description=None, title=None, company_name=None):
    """
    Step 3: Prepare and retrieve all necessary data for processing
    """
    # Get user information
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")
    
    # Get resume data if provided
    resume_data = None
    if resume_id:
        resume = get_resume_by_id(resume_id)
        if not resume:
            raise ValueError(f"Resume {resume_id} not found")
        resume_data = {
            'id': resume['id'],
            'parsed_text': resume.get('parsed_text', ''),
            'file_path': resume.get('file_path', ''),
            'original_filename': resume.get('original_filename', '')
        }
    else:
        # If no resume_id provided, create empty resume data
        resume_data = {
            'id': None,
            'parsed_text': '',
            'file_path': '',
            'original_filename': ''
        }
    
    # Prepare job data structure
    job_data = {
        'user': {
            'id': user['id'],
            'email': user.get('email', ''),
            'name': user.get('name', '')
        },
        'resume': resume_data,
        'job_description': job_description,
        'title': title,
        'company_name': company_name
    }
    
    return job_data
