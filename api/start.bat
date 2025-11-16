@echo off
echo ========================================
echo  Starting Masterpost API (Qwen Only)
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and configure your keys.
    pause
    exit /b 1
)

REM Start server
echo Starting server on http://localhost:8000
echo.
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
