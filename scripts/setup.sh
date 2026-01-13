#!/bin/bash

echo "========================================"
echo "Setup PLN Trend Analysis System"
echo "========================================"
echo ""

# Setup Backend
echo "[1/4] Setup Backend..."
cd backend

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Gagal install dependencies Python!"
    exit 1
fi

# Setup database migrations
echo ""
echo "[2/4] Setup Database Migrations..."
alembic upgrade head
if [ $? -ne 0 ]; then
    echo "ERROR: Gagal menjalankan migrations!"
    echo "Pastikan database sudah dibuat dan .env sudah dikonfigurasi."
    exit 1
fi

# Import data Excel
echo ""
echo "[3/4] Import Data Excel..."
python scripts/import_excel.py
if [ $? -ne 0 ]; then
    echo "ERROR: Gagal import data Excel!"
    echo "Pastikan file Excel ada di folder data."
    exit 1
fi

cd ..

# Setup Frontend
echo ""
echo "[4/4] Setup Frontend..."
cd frontend

# Install dependencies
echo "Installing Node dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "ERROR: Gagal install dependencies Node!"
    exit 1
fi

cd ..

echo ""
echo "========================================"
echo "Setup Selesai!"
echo "========================================"
echo ""
echo "Untuk menjalankan sistem:"
echo ""
echo "Backend:"
echo "  cd backend"
echo "  uvicorn main:app --reload"
echo ""
echo "Frontend (terminal baru):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Backend akan berjalan di: http://localhost:8000"
echo "Frontend akan berjalan di: http://localhost:3000"
echo ""

