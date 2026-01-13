from database import SessionLocal
from models import Customer2024
try:
    db = SessionLocal()
    count = db.query(Customer2024).count()
    print(f"COUNT: {count}")
except Exception as e:
    print(f"ERROR: {e}")
finally:
    db.close()
