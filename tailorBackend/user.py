"""
User CRUD operations
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from database import get_db_connection
import uuid
from datetime import datetime


def create_user(email, password_hash=None, name=None):
    """Create a new user"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("""
            INSERT INTO users (email, password_hash, name)
            VALUES (%s, %s, %s)
            RETURNING *;
        """, (email, password_hash, name))
        
        user = cur.fetchone()
        conn.commit()
        return dict(user)
    except psycopg2.IntegrityError as e:
        conn.rollback()
        raise ValueError(f"User with email {email} already exists")
    except psycopg2.Error as e:
        conn.rollback()
        raise Exception(f"Error creating user: {e}")
    finally:
        cur.close()
        conn.close()


def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
        user = cur.fetchone()
        return dict(user) if user else None
    except psycopg2.Error as e:
        raise Exception(f"Error getting user: {e}")
    finally:
        cur.close()
        conn.close()


def get_user_by_email(email):
    """Get user by email"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
        user = cur.fetchone()
        return dict(user) if user else None
    except psycopg2.Error as e:
        raise Exception(f"Error getting user: {e}")
    finally:
        cur.close()
        conn.close()


def get_all_users():
    """Get all users"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("SELECT * FROM users ORDER BY created_at DESC;")
        users = cur.fetchall()
        return [dict(user) for user in users]
    except psycopg2.Error as e:
        raise Exception(f"Error getting users: {e}")
    finally:
        cur.close()
        conn.close()


def update_user(user_id, email=None, password_hash=None, name=None):
    """Update user information"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        updates = []
        params = []
        
        if email is not None:
            updates.append("email = %s")
            params.append(email)
        if password_hash is not None:
            updates.append("password_hash = %s")
            params.append(password_hash)
        if name is not None:
            updates.append("name = %s")
            params.append(name)
        
        if not updates:
            return get_user_by_id(user_id)
        
        updates.append("updated_at = NOW()")
        params.append(user_id)
        
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s RETURNING *;"
        cur.execute(query, params)
        
        user = cur.fetchone()
        conn.commit()
        return dict(user) if user else None
    except psycopg2.IntegrityError as e:
        conn.rollback()
        raise ValueError(f"Email already exists")
    except psycopg2.Error as e:
        conn.rollback()
        raise Exception(f"Error updating user: {e}")
    finally:
        cur.close()
        conn.close()


def delete_user(user_id):
    """Delete a user (cascades to resumes and jobs)"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
        conn.commit()
        return cur.rowcount > 0
    except psycopg2.Error as e:
        conn.rollback()
        raise Exception(f"Error deleting user: {e}")
    finally:
        cur.close()
        conn.close()

