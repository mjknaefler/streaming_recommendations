# setup database and run schema

import sys
import os
import subprocess
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()

def create_db():
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    
    print(f"Creating database {db_name}...")
    
    cmd = ['psql', '-h', db_host, '-p', db_port, '-U', db_user, '-d', 'postgres', 
           '-c', f"CREATE DATABASE {db_name};"]
    
    # use PGPASSWORD env var so it doesn't prompt
    env = os.environ.copy()
    env['PGPASSWORD'] = db_password

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, env=env)
        print(f"Database {db_name} created")
        return True
    except subprocess.CalledProcessError as e:
        if 'already exists' in e.stderr:
            print(f"Database {db_name} already exists")
            return True
        else:
            print(f"Error: {e.stderr}")
            return False


def run_schema(sql_file='schema.sql'):
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    
    print(f"Running {sql_file}...")
    
    cmd = ['psql', '-h', db_host, '-p', db_port, '-U', db_user, '-d', db_name, '-f', sql_file]
    
    env = os.environ.copy()
    env['PGPASSWORD'] = db_password

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, env=env)
        print(result.stdout)
        print("Schema created!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False


def test_connection():
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    try:
        from models import get_session
        db = get_session()
        db.execute(text("SELECT 1"))
        db.close()
        print("Database connected!")
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False


if __name__ == '__main__':
    print("Setting up database...")
    
    if not create_db():
        print("Failed to create database")
        sys.exit(1)
    
    if not run_schema():
        print("Failed to create schema")
        sys.exit(1)
    
    print("\nTesting connection...")
    if not test_connection():
        print("Connection test failed")
        sys.exit(1)
    
    print("\nAll set! Next: python scripts/seed_data.py")