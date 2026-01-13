@echo off
echo ========================================
echo Setup Database PostgreSQL untuk PLN Trend Analysis
echo ========================================
echo.

REM Cek apakah PostgreSQL terinstall
where psql >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: PostgreSQL tidak ditemukan!
    echo Silakan install PostgreSQL terlebih dahulu.
    echo Download dari: https://www.postgresql.org/download/windows/
    pause
    exit /b 1
)

echo PostgreSQL ditemukan!
echo.

REM Minta input password PostgreSQL superuser
set /p PG_PASSWORD="Masukkan password PostgreSQL superuser (postgres): "

echo.
echo Membuat database dan user...
echo.

REM Jalankan script SQL
psql -U postgres -h localhost -f setup_database.sql

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Gagal membuat database!
    echo Pastikan PostgreSQL berjalan dan password benar.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Database berhasil dibuat!
echo Database: pln_trend_db
echo User: pln_user
echo Password: pln_password
echo ========================================
echo.
pause

