@echo off
call .venv\Scripts\activate
python -m uvicorn backend.app.main:app --reload
pause
