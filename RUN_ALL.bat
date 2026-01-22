@echo off
echo ==================================================
echo AUTOMATED SETUP AND START
echo ==================================================
echo.

echo [1/4] Installing Python dependencies...
pip install -r backend/requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Error installing dependencies!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/4] Setting up Database...
echo Finding credentials...
python backend/scripts/check_postgres.py
echo Creating database if missing...
python backend/scripts/create_db.py
if %ERRORLEVEL% NEQ 0 (
    echo Error setting up database!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [3/4] Importing Full Excel Data...
python backend/scripts/import_excel_full.py
if %ERRORLEVEL% NEQ 0 (
    echo Error importing data!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [4/4] Starting System...
call scripts/start.bat
