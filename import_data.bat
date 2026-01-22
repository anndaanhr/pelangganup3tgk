@echo off
echo ==========================================
echo       MEMPERBAIKI DATA YANG KOSONG
echo ==========================================
echo.
echo Sedang memeriksa database...
cd backend
python scripts/import_excel_full.py
echo.
echo.
echo ==========================================
echo       SELESAI! SILAKAN REFRESH WEB
echo ==========================================
pause
