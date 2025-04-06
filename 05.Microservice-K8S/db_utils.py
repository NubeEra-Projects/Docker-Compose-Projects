"""
Database utility functions for future PostgreSQL integration
"""
import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

# This module provides utility functions for database operations
# For the MVP, we're using in-memory storage, but these functions
# will be used when we transition to PostgreSQL

def get_db_config():
    """Get database configuration from environment variables"""
    return {
        'dbname': os.environ.get('PGDATABASE'),
        'user': os.environ.get('PGUSER'),
        'password': os.environ.get('PGPASSWORD'),
        'host': os.environ.get('PGHOST'),
        'port': os.environ.get('PGPORT', 5432)
    }

@contextmanager
def get_db_connection():
    """
    Context manager for database connections
    
    Usage:
        with get_db_connection() as conn:
            # use connection
    """
    conn = None
    try:
        config = get_db_config()
        conn = psycopg2.connect(**config)
        yield conn
    except psycopg2.Error as e:
        logging.error(f"Database connection error: {e}")
        raise
    finally:
        if conn is not None:
            conn.close()

@contextmanager
def get_db_cursor(commit=False):
    """
    Context manager for database cursors
    
    Usage:
        with get_db_cursor(commit=True) as cursor:
            # use cursor
    """
    with get_db_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            if commit:
                conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
            logging.error(f"Database error: {e}")
            raise
        finally:
            cursor.close()

def execute_sql_file(filename):
    """Execute SQL statements from a file"""
    try:
        with open(filename, 'r') as f:
            sql = f.read()
            
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(sql)
            logging.info(f"Successfully executed SQL file: {filename}")
    except Exception as e:
        logging.error(f"Error executing SQL file {filename}: {e}")
        raise

def initialize_db():
    """Initialize the database with sample data"""
    try:
        execute_sql_file('data.sql')
        logging.info("Database initialized successfully")
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")
        raise
