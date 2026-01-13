@echo off
echo ========================================
echo Setup PLN Trend Analysis System
echo ========================================
echo.

REM Setup Backend
echo [1/4] Setup Backend...
cd backend

REM Install dependencies
echo Installing Python dependencies...
python -m pip install -r requirements.txt --user
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Gagal install dependencies Python!
    pause
    exit /b 1
)

REM Setup database migrations
echo.
echo [2/4] Setup Database Migrations...
python -m alembic upgrade head
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Gagal menjalankan migrations!
    echo Pastikan database sudah dibuat dan .env sudah dikonfigurasi.
    pause
    exit /b 1
)

REM Import data Excel
echo.
echo [3/4] Import Data Excel...
python scripts/import_excel.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Gagal import data Excel!
    echo Pastikan file Excel ada di folder data.
    pause
    exit /b 1
)

cd ..

REM Setup Frontend
echo.
echo [4/4] Setup Frontend...
cd frontend

REM Install dependencies
echo Installing Node dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Gagal install dependencies Node!
    pause
    exit /b 1
)

cd ..

echo.
echo ========================================
echo Setup Selesai!
echo ========================================
echo.
echo Untuk menjalankan sistem:
echo.
echo Backend:
echo   cd backend
echo   python -m uvicorn main:app --reload
echo.
echo Frontend (terminal baru):
echo   cd frontend
echo   npm run dev
echo.
echo Backend akan berjalan di: http://localhost:8000
echo Frontend akan berjalan di: http://localhost:3000
echo.
pause

