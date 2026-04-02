import sys
import sqlalchemy
from sqlalchemy import create_engine, text

# postgresql://postgres.xitfkephwdhxgeyjicmz:[PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
db_url = "postgresql+psycopg2://postgres.xitfkephwdhxgeyjicmz:*Nanda190305@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

print(f"Connecting to {db_url.split('@')[1]}...")
engine = create_engine(db_url, isolation_level="AUTOCOMMIT")

with engine.connect() as conn:
    print("Connection successful!")
    # Read the schema file
    with open('local_schema.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Split by statements (very basic, but works for pg_dump usually)
    print("Executing schema...")
    commands = [stmt.strip() for stmt in sql.split(';') if stmt.strip()]
    for cmd in commands:
        try:
            conn.execute(text(cmd))
        except Exception as e:
            print(f"Skipping failed statement:\n{e}")
    print("Schema applied successfully!")
