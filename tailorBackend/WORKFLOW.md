# Job Processing Workflow

This document outlines the step-by-step process for handling a job tailoring request in the backend.

## 🎯 Entry Point

When a user submits a job request, the backend receives:
- `user_id` (from authenticated session)
- `resume_id` (selected resume to tailor)
- `job_description` (the job posting text)
- `title` (optional - job title)
- `company_name` (optional - company name)

## 📋 Processing Steps

### Step 1: Validation ✅
**Location:** `job_processor.validate_job_request()`

- Validate that the user exists
- Validate that the resume exists (if provided)
- Validate that the resume belongs to the user
- Validate that job description is provided and not empty

**If validation fails:** Return error response, do not create job

---

### Step 2: Create Job Record 📝
**Location:** `job.create_job()`

- Create a new job record in the database
- Set status to `PENDING`
- Store all provided information (user_id, resume_id, job_description, etc.)
- Return the created job with its ID

**Database State:** Job exists with status = 'PENDING'

---

### Step 3: Prepare Job Data 📦
**Location:** `job_processor.prepare_job_data()`

- Fetch user information from database
- Fetch resume data (parsed_text, file_path, etc.)
- Organize all data into a structured format for processing

**Data Structure:**
```python
{
    'user': {...},
    'resume': {...},
    'job_description': '...',
    'title': '...',
    'company_name': '...'
}
```

---

### Step 4: Process Tailoring 🔧
**Location:** `job_processor.process_job_tailoring()`

This is where the actual tailoring logic happens:

1. **Extract Resume Content**
   - Read `parsed_text` from resume
   - Or parse resume file from `file_path` if parsed_text not available

2. **Analyze Job Description**
   - Extract key requirements
   - Identify skills, experience needed
   - Note important keywords

3. **Tailor Resume**
   - Match resume content to job requirements
   - Highlight relevant experience
   - Reorder/emphasize sections
   - Generate tailored content

4. **Format Output**
   - Structure the tailored resume
   - Ensure proper formatting

**Current Implementation:** Placeholder that returns formatted text
**Future Implementation:** Would integrate with AI/ML service or custom logic

---

### Step 5: Save Results ✅
**Location:** `job.complete_job()`

- Update job record with `tailored_resume_text`
- Set status to `COMPLETED`
- Update `updated_at` timestamp

**Database State:** Job status = 'COMPLETED' with tailored resume stored

---

## 🔄 Alternative Flows

### Async Processing
If `process_immediately=False`:
1. Create job with `PENDING` status
2. Return job ID immediately
3. Process later via `process_pending_job(job_id)`
4. Useful for background jobs or queue systems

### Error Handling
If any step fails:
1. Mark job as `FAILED` using `job.mark_job_as_failed()`
2. Log the error
3. Return error response to user

### Retry Logic
For failed jobs:
1. Retrieve job with `get_job_by_id(job_id)`
2. Check status is `FAILED` or `PENDING`
3. Call `process_pending_job(job_id)` to retry

---

## 🚀 Usage Examples

### Immediate Processing
```python
from job_processor import process_job

job = process_job(
    user_id="user-uuid",
    resume_id="resume-uuid",
    title="Software Engineer",
    company_name="Tech Corp",
    job_description="We are looking for...",
    process_immediately=True
)
# Job is created and processed immediately
```

### Async Processing
```python
from job_processor import process_job, process_pending_job

# Create job, leave as pending
job = process_job(
    user_id="user-uuid",
    resume_id="resume-uuid",
    job_description="We are looking for...",
    process_immediately=False  # Don't process now
)

# Process later (e.g., in background worker)
completed_job = process_pending_job(job['id'])
```

---

## 📊 Database Status Flow

```
PENDING → (processing) → COMPLETED
   ↓
FAILED
```

- **PENDING**: Job created, waiting to be processed
- **COMPLETED**: Processing finished, tailored resume ready
- **FAILED**: Processing encountered an error

---

## 🔌 Integration Points

### Where to Start
1. **API Endpoint** receives request
2. **Call `process_job()`** from `job_processor.py`
3. **Return job ID** (or full job object)

### Next Steps to Implement
1. **Resume Parsing**: Extract text from PDF/Word files
2. **Job Description Analysis**: Parse and extract requirements
3. **Tailoring Algorithm**: Implement actual customization logic
4. **Background Processing**: Add queue system for async jobs
5. **Error Handling**: Comprehensive error handling and logging
6. **Notifications**: Notify user when job completes

---

## 📝 Notes

- The current `process_job_tailoring()` function is a placeholder
- Replace it with your actual tailoring logic
- Consider adding progress tracking for long-running jobs
- Add logging at each step for debugging
- Consider rate limiting for job processing

