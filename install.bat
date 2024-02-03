@echo off

REM Check if python is installed
python --version >nul 2>&1
if errorlevel 1 echo Python is not installed. Please install Python first. && exit /b

REM Create a virtual environment
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate

REM Install the necessary libraries
pip install pillow gradio

REM Deactivate the virtual environment
deactivate

echo.
echo Setup is complete. You can now run the app by activating the virtual environment and running the python script.
echo To activate the virtual environment, use: call venv\Scripts\activate
echo To run the app, use: python app.py