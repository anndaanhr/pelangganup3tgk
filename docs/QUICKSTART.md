# Quick Start Guide - PLN Trend Analysis

Panduan cepat untuk menjalankan sistem PLN Trend Analysis.

## Opsi 1: Menggunakan Docker (Recommended)

### Prerequisites
- Docker Desktop terinstall
- Python 3.11+
- Node.js 18+

### Langkah-langkah:

1. **Setup Database dengan Docker:**
   ```bash
   docker-compose up -d postgres
   ```

2. **Setup Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   alembic upgrade head
   python scripts/import_excel.py
   ```

3. **Setup Frontend:**
   ```bash
   cd frontend
   npm install
   ```

4. **Jalankan Sistem:**

   **Windows:**
   ```bash
   start.bat
   ```

   **Linux/Mac:**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

   Atau manual:
   - Terminal 1 (Backend):
     ```bash
     cd backend
     uvicorn main:app --reload
     ```
   
   - Terminal 2 (Frontend):
     ```bash
     cd frontend
     npm run dev
     ```

## Opsi 2: PostgreSQL Manual

### Prerequisites
- PostgreSQL 15+ terinstall dan berjalan
- Python 3.11+
- Node.js 18+

### Langkah-langkah:

1. **Setup Database:**

   **Windows:**
   ```bash
   setup_database.bat
   ```

   **Linux/Mac:**
   ```bash
   chmod +x setup_database.sh
   ./setup_database.sh
   ```

   Atau manual:
   ```bash
   psql -U postgres -f setup_database.sql
   ```

2. **Setup Lengkap:**

   **Windows:**
   ```bash
   setup.bat
   ```

   **Linux/Mac:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Jalankan Sistem:**

   - Terminal 1 (Backend):
     ```bash
     cd backend
     python -m uvicorn main:app --reload
     ```
   
   - Terminal 2 (Frontend):
     ```bash
     cd frontend
     npm run dev
     ```

## Akses Sistem

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## Troubleshooting

### Database Connection Error
- Pastikan PostgreSQL berjalan
- Cek file `backend/.env` dengan kredensial yang benar
- Untuk Docker: pastikan container `pln_postgres` berjalan (`docker ps`)

### Import Excel Error
- Pastikan file Excel ada di folder root: `JUAL PERPELANGGAN 2024 BL.xlsx` dan `JUAL PERPELANGGAN 2025 BL.xlsx`
- Pastikan pandas dan openpyxl terinstall

### Port Already in Use
- Backend (8000): Tutup aplikasi lain yang menggunakan port 8000
- Frontend (3000): Tutup aplikasi lain yang menggunakan port 3000
- PostgreSQL (5432): Pastikan tidak ada instance PostgreSQL lain yang berjalan

## File Konfigurasi

- **Database:** `backend/.env` (DATABASE_URL)
- **Frontend API:** `frontend/.env.local` (NEXT_PUBLIC_API_URL, optional)

## Default Credentials

- **Database:** pln_trend_db
- **User:** pln_user
- **Password:** pln_password
- **Host:** localhost
- **Port:** 5432

**PENTING:** Ganti password default di production!

