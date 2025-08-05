@echo off

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

REM Install dependencies
pip install -r requirements.txt

REM Run the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
