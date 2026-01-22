import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

# Read creds from file or use defaults
user = "postgres"
password = "pln_password" # Default fallback, but likely wrong. Expect pg_creds.txt
try:
    with open("pg_creds.txt", "r") as f:
        lines = f.read().splitlines()
        if len(lines) >= 2:
            user = lines[0]
            password = lines[1]
            print(f"Using found credentials: {user}")
except:
    print("Credentials file not found, trying defaults...")
    # Try expected defaults if file missing
    user = "postgres" 
    password = "" 

try:
    # Connect to default 'postgres' db
    conn = psycopg2.connect(
        dbname="postgres",
        user=user,
        password=password,
        host="localhost",
        port="5432"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    # 1. Create Database
    try:
        cur.execute("CREATE DATABASE pln_trend_db")
        print("Database 'pln_trend_db' created successfully.")
    except psycopg2.errors.DuplicateDatabase:
        print("Database 'pln_trend_db' already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")

    # 2. Create User
    try:
        cur.execute("CREATE USER pln_user WITH PASSWORD 'pln_password'")
        print("User 'pln_user' created successfully.")
    except psycopg2.errors.DuplicateObject:
        print("User 'pln_user' already exists.")
    except Exception as e:
        print(f"Error creating user: {e}")

    # 3. Grant Privileges (Approximation for simplicity)
    try:
        cur.execute("GRANT ALL PRIVILEGES ON DATABASE pln_trend_db TO pln_user")
        print("Granted privileges on database.")
    except Exception as e:
        print(f"Error granting database privileges: {e}")
        
    cur.close()
    conn.close()
    
    # Verify connection as new user
    print("Verifying new user connection...")
    conn = psycopg2.connect(
        dbname="pln_trend_db",
        user="pln_user",
        password="pln_password",
        host="localhost",
        port="5432"
    )
    conn.close()
    print("SUCCESS: Database and User setup complete!")
    
except Exception as e:
    print(f"FATAL ERROR during setup: {e}")
    sys.exit(1)
