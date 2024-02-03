@echo off

REM Activate the virtual environment
call venv\Scripts\activate

REM Run the app
python app.py

REM Deactivate the virtual environment
deactivate