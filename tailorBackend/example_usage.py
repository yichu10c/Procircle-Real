"""
Example usage of the database functions
"""
from database import create_tables, drop_tables
from user import create_user, get_user_by_email, delete_user
from resume import create_resume, get_resumes_by_user_id, delete_resume
from job import create_job, get_job_with_relations, complete_job, get_jobs_by_user_id, delete_job


def example_workflow():
    """Example workflow demonstrating the Job-centric architecture"""
    
    print("=" * 60)
    print("Example Workflow: Resume Tailoring Session")
    print("=" * 60)
    
    # Step 1: Create tables (if not already created)
    print("\n📝 Step 1: Creating database tables...")
    try:
        create_tables()
    except Exception as e:
        print(f"   Note: {e}")
    
    # Step 2: Create a user
    print("\n👤 Step 2: Creating user...")
    try:
        user = create_user(
            email="john.doe@example.com",
            password_hash="hashed_password_here",
            name="John Doe"
        )
        print(f"   ✅ User created: {user['id']} ({user['email']})")
        user_id = user['id']
    except ValueError as e:
        print(f"   User might already exist, fetching...")
        user = get_user_by_email("john.doe@example.com")
        if user:
            user_id = user['id']
            print(f"   ✅ Found user: {user_id} ({user['email']})")
        else:
            raise
    
    # Step 3: Upload a resume
    print("\n📄 Step 3: Creating resume...")
    resume = create_resume(
        user_id=user_id,
        file_path="https://storage.example.com/resumes/john-doe-resume.pdf",
        original_filename="john-doe-resume.pdf",
        parsed_text="John Doe\nSoftware Engineer\n..."
    )
    print(f"   ✅ Resume created: {resume['id']} ({resume['original_filename']})")
    resume_id = resume['id']
    
    # Step 4: Create a job tailoring session
    print("\n💼 Step 4: Creating job tailoring session...")
    job = create_job(
        user_id=user_id,
        resume_id=resume_id,
        title="Senior Software Engineer",
        company_name="Tech Corp",
        job_description="We are looking for a Senior Software Engineer with 5+ years of experience...",
        status="PENDING"
    )
    print(f"   ✅ Job created: {job['id']}")
    print(f"   Status: {job['status']}")
    job_id = job['id']
    
    # Step 5: Complete the job with tailored resume
    print("\n✨ Step 5: Completing job with tailored resume...")
    completed_job = complete_job(
        job_id=job_id,
        tailored_resume_text="John Doe\nSenior Software Engineer\n[Tailored content...]"
    )
    print(f"   ✅ Job completed: {completed_job['status']}")
    
    # Step 6: Get job with all relations
    print("\n🔍 Step 6: Retrieving job with all relations...")
    job_details = get_job_with_relations(job_id)
    if job_details:
        print(f"   Job ID: {job_details['id']}")
        print(f"   Title: {job_details['title']}")
        print(f"   Status: {job_details['status']}")
        print(f"   User: {job_details['user']['email']}")
        print(f"   Resume: {job_details['resume']['original_filename']}")
    
    # Step 7: Get all jobs for user
    print("\n📋 Step 7: Getting all jobs for user...")
    user_jobs = get_jobs_by_user_id(user_id)
    print(f"   ✅ Found {len(user_jobs)} job(s) for user")
    for idx, j in enumerate(user_jobs, 1):
        print(f"   {idx}. {j['title']} at {j['company_name']} - {j['status']}")
    
    print("\n" + "=" * 60)
    print("✅ Workflow completed successfully!")
    print("=" * 60)
    
    # Cleanup (optional - comment out to keep data)
    # print("\n🧹 Cleaning up...")
    # delete_job(job_id)
    # delete_resume(resume_id)
    # delete_user(user_id)
    # print("✅ Cleanup complete")


if __name__ == "__main__":
    example_workflow()

