#!/bin/bash

echo "========================================"
echo "Starting PLN Trend Analysis System"
echo "========================================"
echo ""

# Start PostgreSQL dengan Docker (jika menggunakan Docker)
if command -v docker &> /dev/null; then
    echo "Docker ditemukan. Menggunakan Docker untuk PostgreSQL..."
    docker-compose up -d postgres
    echo "Menunggu PostgreSQL siap..."
    sleep 5
else
    echo "Docker tidak ditemukan. Pastikan PostgreSQL berjalan secara manual."
fi

# Start Backend
echo ""
echo "Starting Backend..."
cd backend
uvicorn main:app --reload &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 3

# Start Frontend
echo ""
echo "Starting Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "System Started!"
echo "========================================"
echo ""
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Tekan Ctrl+C untuk menghentikan semua service."

# Trap untuk cleanup saat exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; docker-compose down 2>/dev/null; exit" INT TERM

# Wait for processes
wait

