import asyncio
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User
import bcrypt
from database import DATABASE_URL

print(f"Connecting to database: {DATABASE_URL}")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_initial_user():
    # Buat tabel jika belum ada (hanya tabel User jika tabel lain sudah ada)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Cek apakah user sudah ada
        existing_user = db.query(User).filter(User.username == "tjgkrg").first()
        if existing_user:
            print("User 'tjgkrg' already exists.")
            return

        # Buat hashed password untuk '123456'
        password = "123456".encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
        
        new_user = User(username="tjgkrg", hashed_password=hashed, role="admin")
        db.add(new_user)
        db.commit()
        print("Default user 'tjgkrg' created successfully with password '123456'.")
    except Exception as e:
        print(f"Error creating user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_user()
