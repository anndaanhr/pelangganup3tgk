import psycopg2
import sys

def test_conn(user, password):
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host="localhost",
            port="5432"
        )
        print(f"SUCCESS: Connected with user='{user}', password='{password}'")
        conn.close()
        return True
    except Exception as e:
        print(f"FAILED: Connected with user='{user}', password='{password}': {e}")
        return False

# Try common defaults
creds = [
    ("postgres", "postgres"),
    ("postgres", ""),
    ("root", ""),
]

for user, pwd in creds:
    if test_conn(user, pwd):
        # Write successful creds to file
        with open("pg_creds.txt", "w") as f:
            f.write(f"{user}\n{pwd}")
        sys.exit(0)

sys.exit(1)
