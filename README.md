# AgroSense AI — Simple UI Version

This version follows the project flow used in the AgroSenseAI presentation:

**Streamlit frontend → FastAPI backend → ML models → PostgreSQL history**

The interface contains only:

- Home
- Crop Recommendation
- Yield Prediction
- Prediction History
- About

No React dashboard, charts, weather API, maps, authentication, or other extra features are included.

## 1. Create and activate the virtual environment

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 2. Install dependencies

```powershell
pip install -r requirements.txt
```

## 3. PostgreSQL

Create the database:

```sql
CREATE DATABASE agrosense_ai;
```

Copy `.env.example` to `.env` and update your password:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/agrosense_ai
```

The backend creates the prediction table automatically when it starts. The same table definition is also included in `database/init.sql` for the project structure shown in the presentation.

## 4. Start the backend

```powershell
python -m uvicorn backend.app.main:app --reload
```

Backend API docs:

`http://127.0.0.1:8000/docs`

## 5. Start the Streamlit frontend

Open a second terminal, activate `.venv`, then run:

```powershell
streamlit run frontend/app.py
```

Frontend:

`http://localhost:8501`

## Easy Windows start

After the one-time setup above, double-click:

`START_AGROSENSE.bat`

It opens the backend and frontend in separate terminals.
