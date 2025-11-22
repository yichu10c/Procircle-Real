"""
Resume CRUD operations
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from database import get_db_connection


def create_resume(user_id, file_path, original_filename=None, parsed_text=None):
    """Create a new resume"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("""
            INSERT INTO resumes (user_id, file_path, original_filename, parsed_text)
            VALUES (%s, %s, %s, %s)
            RETURNING *;
        """, (user_id, file_path, original_filename, parsed_text))
        
        resume = cur.fetchone()
        conn.commit()
        return dict(resume)
    except psycopg2.Error as e:
        conn.rollback()
        raise Exception(f"Error creating resume: {e}")
    finally:
        cur.close()
        conn.close()


def get_resume_by_id(resume_id):
    """Get resume by ID"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("SELECT * FROM resumes WHERE id = %s;", (resume_id,))
        resume = cur.fetchone()
        return dict(resume) if resume else None
    except psycopg2.Error as e:
        raise Exception(f"Error getting resume: {e}")
    finally:
        cur.close()
        conn.close()


def get_resumes_by_user_id(user_id):
    """Get all resumes for a user"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("""
            SELECT * FROM resumes 
            WHERE user_id = %s 
            ORDER BY created_at DESC;
        """, (user_id,))
        resumes = cur.fetchall()
        return [dict(resume) for resume in resumes]
    except psycopg2.Error as e:
        raise Exception(f"Error getting resumes: {e}")
    finally:
        cur.close()
        conn.close()


def get_all_resumes():
    """Get all resumes"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("SELECT * FROM resumes ORDER BY created_at DESC;")
        resumes = cur.fetchall()
        return [dict(resume) for resume in resumes]
    except psycopg2.Error as e:
        raise Exception(f"Error getting resumes: {e}")
    finally:
        cur.close()
        conn.close()


def update_resume(resume_id, file_path=None, original_filename=None, parsed_text=None):
    """Update resume information"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        updates = []
        params = []
        
        if file_path is not None:
            updates.append("file_path = %s")
            params.append(file_path)
        if original_filename is not None:
            updates.append("original_filename = %s")
            params.append(original_filename)
        if parsed_text is not None:
            updates.append("parsed_text = %s")
            params.append(parsed_text)
        
        if not updates:
            return get_resume_by_id(resume_id)
        
        updates.append("updated_at = NOW()")
        params.append(resume_id)
        
        query = f"UPDATE resumes SET {', '.join(updates)} WHERE id = %s RETURNING *;"
        cur.execute(query, params)
        
        resume = cur.fetchone()
        conn.commit()
        return dict(resume) if resume else None
    except psycopg2.Error as e:
        conn.rollback()
        raise Exception(f"Error updating resume: {e}")
    finally:
        cur.close()
        conn.close()


def delete_resume(resume_id):
    """Delete a resume (sets resume_id to NULL in jobs)"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("DELETE FROM resumes WHERE id = %s;", (resume_id,))
        conn.commit()
        return cur.rowcount > 0
    except psycopg2.Error as e:
        conn.rollback()
        raise Exception(f"Error deleting resume: {e}")
    finally:
        cur.close()
        conn.close()

