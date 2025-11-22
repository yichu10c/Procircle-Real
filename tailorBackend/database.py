"""
Database connection and table creation functions
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'tailor_db'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', ''),
            port=os.getenv('DB_PORT', '5432')
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        raise


def create_tables():
    """Create all database tables"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Create enum type for job status
        cur.execute("""
            DO $$ BEGIN
                CREATE TYPE job_status AS ENUM ('PENDING', 'COMPLETED', 'FAILED');
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)
        
        # Create users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255),
                name VARCHAR(100),
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """)
        
        # Create resumes table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                file_path TEXT NOT NULL,
                original_filename VARCHAR(255),
                parsed_text TEXT,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """)
        
        # Create jobs table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                resume_id UUID REFERENCES resumes(id) ON DELETE SET NULL,
                title VARCHAR(255),
                company_name VARCHAR(255),
                job_description TEXT,
                tailored_resume_text TEXT,
                status job_status DEFAULT 'PENDING',
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """)
        
        # Create indexes
        cur.execute("CREATE INDEX IF NOT EXISTS idx_resumes_user_id ON resumes(user_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_jobs_user_id ON jobs(user_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_jobs_resume_id ON jobs(resume_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
        
        conn.commit()
        print("✅ All tables created successfully!")
        
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error creating tables: {e}")
        raise
    finally:
        cur.close()
        conn.close()


def drop_tables():
    """Drop all database tables (use with caution!)"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Drop tables in reverse order of dependencies
        cur.execute("DROP TABLE IF EXISTS jobs CASCADE;")
        cur.execute("DROP TABLE IF EXISTS resumes CASCADE;")
        cur.execute("DROP TABLE IF EXISTS users CASCADE;")
        cur.execute("DROP TYPE IF EXISTS job_status CASCADE;")
        
        conn.commit()
        print("✅ All tables dropped successfully!")
        
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error dropping tables: {e}")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    # Example usage
    print("Creating database tables...")
    create_tables()

