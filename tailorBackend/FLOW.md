# Backend Flow - Job Processing

This document explains the complete flow from receiving a JSON request to storing the tailored resume.

## 📥 Entry Point: `api_handler.py`

**Function:** `handle_job_request(json_data)`

This is where your backend receives the JSON object from the frontend.

### Expected JSON Input:
```json
{
    "user_id": "uuid-string",
    "resume_id": "uuid-string",
    "title": "Software Engineer",
    "company_name": "Tech Corp",
    "job_description": "We are looking for..."
}
```

---

## 🔄 Complete Flow

```
JSON Request
    ↓
api_handler.py (handle_job_request)
    ↓
job_processor.py (process_job_request)
    ↓
┌─────────────────────────────────────┐
│ STEP 1: Validate Request            │
│ - Check user exists                 │
│ - Check resume exists (if provided) │
│ - Check job_description provided    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ STEP 2: Create Job in Database     │
│ - Create job record                │
│ - Status: PENDING                   │
│ - tailored_resume_text: NULL       │
│ - Store: user_id, resume_id, etc.  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ STEP 3: Prepare Data               │
│ - Fetch user info                   │
│ - Fetch resume (parsed_text)        │
│ - Organize into job_data structure  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ STEP 4: Create Prompt              │
│ - openai_service.py                 │
│ - create_tailoring_prompt()         │
│ - Format prompt with resume +       │
│   job_description                   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ STEP 5: Call OpenAI API            │
│ - openai_service.py                 │
│ - call_openai_api(prompt)           │
│ - Send prompt to OpenAI             │
│ - Receive tailored resume           │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ STEP 6: Store in Database          │
│ - Update job record                 │
│ - Set tailored_resume_text          │
│ - Set status: COMPLETED             │
└─────────────────────────────────────┘
    ↓
Return completed job object
```

---

## 📝 Detailed Steps

### Step 1: Validation (`job_processor.validate_job_request`)
- ✅ User exists in database
- ✅ Resume exists (if resume_id provided)
- ✅ Resume belongs to user
- ✅ Job description is not empty

**If validation fails:** Return error, do not proceed

---

### Step 2: Create Job Record (`job.create_job`)
Creates a new job in the database with:
- `user_id` - from request
- `resume_id` - from request (can be NULL)
- `title` - from request
- `company_name` - from request
- `job_description` - from request
- `status` - set to `'PENDING'`
- `tailored_resume_text` - NULL (will be filled later)

**Database State:** Job exists but is incomplete

---

### Step 3: Prepare Data (`job_processor.prepare_job_data`)
Fetches and organizes:
- User information from database
- Resume data (especially `parsed_text`)
- Job description and metadata

**Output:** `job_data` dictionary with all needed information

---

### Step 4: Create Prompt (`openai_service.create_tailoring_prompt`)
Builds a formatted prompt that includes:
- Job title and company
- Full job description
- Original resume text
- Instructions for tailoring

**Output:** Formatted prompt string

---

### Step 5: Call OpenAI (`openai_service.call_openai_api`)
- Connects to OpenAI API using API key
- Sends the prompt
- Receives tailored resume response
- Handles errors and token usage

**Output:** Tailored resume text

---

### Step 6: Store Results (`job.complete_job`)
- Updates the job record in database
- Sets `tailored_resume_text` to the OpenAI response
- Changes `status` from `'PENDING'` to `'COMPLETED'`
- Updates `updated_at` timestamp

**Database State:** Job is complete with tailored resume

---

## 🚀 Usage Example

```python
from api_handler import handle_job_request

# JSON received from frontend
json_request = {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "resume_id": "660e8400-e29b-41d4-a716-446655440000",
    "title": "Senior Software Engineer",
    "company_name": "Tech Corp",
    "job_description": "We are looking for..."
}

# Process the request
result = handle_job_request(json_request)

# Result contains:
# - job['id']
# - job['status'] = 'COMPLETED'
# - job['tailored_resume_text'] = "..."
```

---

## 🔧 Setup Required

1. **Environment Variables** (`.env` file):
```env
DB_HOST=localhost
DB_NAME=tailor_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
OPENAI_API_KEY=your-openai-api-key
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

3. **Database Tables**:
```bash
python database.py
```

---

## 📊 Database State Flow

```
Before Processing:
┌─────────────────────────────┐
│ Job Record                   │
│ - status: PENDING            │
│ - tailored_resume_text: NULL  │
└─────────────────────────────┘

After Processing:
┌─────────────────────────────┐
│ Job Record                   │
│ - status: COMPLETED          │
│ - tailored_resume_text: "..." │
└─────────────────────────────┘
```

---

## 🎯 Integration Points

### For Flask/FastAPI:
```python
from flask import Flask, request, jsonify
from api_handler import handle_job_request

app = Flask(__name__)

@app.route('/api/jobs', methods=['POST'])
def create_job():
    json_data = request.get_json()
    try:
        result = handle_job_request(json_data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
```

### For Direct Python:
```python
from api_handler import handle_job_request

json_data = {...}  # Your JSON object
result = handle_job_request(json_data)
```

---

## ⚠️ Error Handling

- **Validation errors:** Returned immediately, no job created
- **Processing errors:** Job is marked as `FAILED` in database
- **OpenAI API errors:** Job is marked as `FAILED`, error is logged

---

## 📝 Notes

- The job is created in the database BEFORE processing (Step 2)
- This allows tracking of pending jobs
- If processing fails, the job status is updated to `FAILED`
- The tailored resume is only stored after successful OpenAI response

