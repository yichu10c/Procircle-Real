# Tailor Backend

Backend for a resume tailoring service that manages resume customization for specific job applications.

## 🏗️ Architecture

The backend uses a **Job-centric** model where each tailoring session is represented as a Job that combines:
- A **User** (who owns the job)
- A **Resume** (the base resume to tailor)
- A **Job Description** (the target job posting)
- A **Tailored Resume** (the customized result)

## 📊 Database Schema

### Entities

1. **Users** - User accounts and authentication
2. **Resumes** - Uploaded resumes (reusable across jobs)
3. **Jobs** - Core entity representing a tailoring session

### Relationships

```
User ───< Resume
  │
  └───< Job >── Resume
```

## 🚀 Setup

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   DB_HOST=localhost
   DB_NAME=tailor_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_PORT=5432
   ```

3. **Create the database:**
   ```bash
   # Connect to PostgreSQL and create the database
   createdb tailor_db
   ```

4. **Create the tables:**
   ```bash
   python database.py
   ```

## 📁 File Structure

- `database.py` - Database connection and table creation/dropping functions
- `user.py` - User CRUD operations
- `resume.py` - Resume CRUD operations
- `job.py` - Job CRUD operations (core entity)
- `job_processor.py` - **Job processing service** - Main entry point for processing jobs
- `example_usage.py` - Example workflow demonstrating the system
- `WORKFLOW.md` - Detailed workflow documentation

## 🗄️ Database Schema Details

### Users Table
- Stores user authentication and profile information
- Each user can have multiple resumes and jobs

### Resumes Table
- Stores uploaded resume files
- Can be reused across multiple job applications
- Includes parsed text for processing

### Jobs Table (Core Entity)
- Represents a single tailoring session
- Links a user, a resume, a job description, and a tailored result
- Tracks status (PENDING, COMPLETED, FAILED)
- Stores the tailored resume text

## 💻 Usage Examples

### Create Tables
```python
from database import create_tables
create_tables()
```

### Create a User
```python
from user import create_user
user = create_user(
    email="john@example.com",
    password_hash="hashed_password",
    name="John Doe"
)
```

### Create a Resume
```python
from resume import create_resume
resume = create_resume(
    user_id=user['id'],
    file_path="/path/to/resume.pdf",
    original_filename="resume.pdf",
    parsed_text="..."
)
```

### Create a Job Tailoring Session
```python
from job import create_job, complete_job
job = create_job(
    user_id=user['id'],
    resume_id=resume['id'],
    title="Software Engineer",
    company_name="Tech Corp",
    job_description="We are looking for..."
)

# Later, complete the job
complete_job(
    job_id=job['id'],
    tailored_resume_text="Tailored resume content..."
)
```

### Run Example Workflow
```python
python example_usage.py
```

## 📦 Available Functions

### Database Management
- `create_tables()` - Create all database tables
- `drop_tables()` - Drop all tables (use with caution)
- `get_db_connection()` - Get database connection

### User Operations
- `create_user(email, password_hash, name)`
- `get_user_by_id(user_id)`
- `get_user_by_email(email)`
- `get_all_users()`
- `update_user(user_id, ...)`
- `delete_user(user_id)`

### Resume Operations
- `create_resume(user_id, file_path, original_filename, parsed_text)`
- `get_resume_by_id(resume_id)`
- `get_resumes_by_user_id(user_id)`
- `get_all_resumes()`
- `update_resume(resume_id, ...)`
- `delete_resume(resume_id)`

### Job Operations
- `create_job(user_id, resume_id, title, company_name, job_description, status)`
- `get_job_by_id(job_id)`
- `get_job_with_relations(job_id)` - Get job with user and resume
- `get_jobs_by_user_id(user_id)`
- `get_all_jobs()`
- `update_job(job_id, ...)`
- `complete_job(job_id, tailored_resume_text)`
- `mark_job_as_failed(job_id)`
- `delete_job(job_id)`

## 📦 Tech Stack

- **Language:** Python 3.8+
- **Database:** PostgreSQL
- **Database Driver:** psycopg2
- **Environment:** python-dotenv

## 🔐 Security Notes

- Passwords should be hashed (e.g., using bcrypt) before storing
- Use environment variables for sensitive database credentials
- Consider using connection pooling for production

## 📄 License

ISC
