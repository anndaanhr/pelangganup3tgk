@echo off
echo ========================================
echo Starting PLN Trend Analysis System
echo ========================================
echo.

REM Start PostgreSQL dengan Docker (jika menggunakan Docker)
echo Checking Docker...
docker --version >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Docker ditemukan. Menggunakan Docker untuk PostgreSQL...
    docker-compose up -d postgres
    echo Menunggu PostgreSQL siap...
    timeout /t 5 /nobreak >nul
) else (
    echo Docker tidak ditemukan. Pastikan PostgreSQL berjalan secara manual.
)

REM Start Backend
echo.
echo Starting Backend...
start "PLN Backend" cmd /k "cd backend && python -m uvicorn main:app --reload"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend
echo.
echo Starting Frontend...
start "PLN Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo System Started!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Tekan Ctrl+C untuk menghentikan semua service.
pause

