"""
Job CRUD operations - Core entity for tailoring sessions
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from database import get_db_connection


def create_job(user_id, resume_id=None, title=None, company_name=None, 
               job_description=None, status='PENDING'):
    """Create a new job tailoring session"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("""
            INSERT INTO jobs (user_id, resume_id, title, company_name, job_description, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *;
        """, (user_id, resume_id, title, company_name, job_description, status))
        
        job = cur.fetchone()
        conn.commit()
        return dict(job)
    except psycopg2.Error as e:
        conn.rollback()
        raise Exception(f"Error creating job: {e}")
    finally:
        cur.close()
        conn.close()


def get_job_by_id(job_id):
    """Get job by ID"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("SELECT * FROM jobs WHERE id = %s;", (job_id,))
        job = cur.fetchone()
        return dict(job) if job else None
    except psycopg2.Error as e:
        raise Exception(f"Error getting job: {e}")
    finally:
        cur.close()
        conn.close()


def get_job_with_relations(job_id):
    """Get job with user and resume"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Get job with user and resume
        cur.execute("""
            SELECT 
                j.*,
                json_build_object(
                    'id', u.id,
                    'email', u.email,
                    'name', u.name
                ) as user,
                json_build_object(
                    'id', r.id,
                    'original_filename', r.original_filename,
                    'file_path', r.file_path,
                    'parsed_text', r.parsed_text
                ) as resume
            FROM jobs j
            LEFT JOIN users u ON j.user_id = u.id
            LEFT JOIN resumes r ON j.resume_id = r.id
            WHERE j.id = %s;
        """, (job_id,))
        
        job = cur.fetchone()
        return dict(job) if job else None
    except psycopg2.Error as e:
        raise Exception(f"Error getting job: {e}")
    finally:
        cur.close()
        conn.close()


def get_jobs_by_user_id(user_id):
    """Get all jobs for a user"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("""
            SELECT 
                j.*,
                json_build_object(
                    'id', r.id,
                    'original_filename', r.original_filename
                ) as resume
            FROM jobs j
            LEFT JOIN resumes r ON j.resume_id = r.id
            WHERE j.user_id = %s 
            ORDER BY j.created_at DESC;
        """, (user_id,))
        jobs = cur.fetchall()
        return [dict(job) for job in jobs]
    except psycopg2.Error as e:
        raise Exception(f"Error getting jobs: {e}")
    finally:
        cur.close()
        conn.close()


def get_all_jobs():
    """Get all jobs"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("SELECT * FROM jobs ORDER BY created_at DESC;")
        jobs = cur.fetchall()
        return [dict(job) for job in jobs]
    except psycopg2.Error as e:
        raise Exception(f"Error getting jobs: {e}")
    finally:
        cur.close()
        conn.close()


def update_job(job_id, title=None, company_name=None, job_description=None,
               tailored_resume_text=None, status=None):
    """Update job information"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = %s")
            params.append(title)
        if company_name is not None:
            updates.append("company_name = %s")
            params.append(company_name)
        if job_description is not None:
            updates.append("job_description = %s")
            params.append(job_description)
        if tailored_resume_text is not None:
            updates.append("tailored_resume_text = %s")
            params.append(tailored_resume_text)
        if status is not None:
            updates.append("status = %s")
            params.append(status)
        
        if not updates:
            return get_job_by_id(job_id)
        
        updates.append("updated_at = NOW()")
        params.append(job_id)
        
        query = f"UPDATE jobs SET {', '.join(updates)} WHERE id = %s RETURNING *;"
        cur.execute(query, params)
        
        job = cur.fetchone()
        conn.commit()
        return dict(job) if job else None
    except psycopg2.Error as e:
        conn.rollback()
        raise Exception(f"Error updating job: {e}")
    finally:
        cur.close()
        conn.close()


def complete_job(job_id, tailored_resume_text):
    """Mark job as completed with tailored resume"""
    return update_job(
        job_id=job_id,
        tailored_resume_text=tailored_resume_text,
        status='COMPLETED'
    )


def mark_job_as_failed(job_id):
    """Mark job as failed"""
    return update_job(job_id=job_id, status='FAILED')


def delete_job(job_id):
    """Delete a job"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("DELETE FROM jobs WHERE id = %s;", (job_id,))
        conn.commit()
        return cur.rowcount > 0
    except psycopg2.Error as e:
        conn.rollback()
        raise Exception(f"Error deleting job: {e}")
    finally:
        cur.close()
        conn.close()

