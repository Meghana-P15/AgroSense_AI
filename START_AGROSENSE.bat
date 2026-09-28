@echo off
start "AgroSense Backend" cmd /k "call .venv\Scripts\activate && python -m uvicorn backend.app.main:app --reload"
timeout /t 3 /nobreak >nul
start "AgroSense Frontend" cmd /k "call .venv\Scripts\activate && streamlit run frontend\app.py"
