@echo off

REM Check if virtual environment exists, if not create it
if not exist venv (
    echo Virtual environment not found. Creating one...
    python -m venv venv
)

REM Activate the virtual environment
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo Failed to activate the virtual environment.
    exit /b 1
)

REM Install required packages
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo requirements.txt not found. Skipping package installation.
)

REM Run the setup_mgmt.py script
python interview_prep\setup_mgmt.py

REM Deactivate the virtual environment
if defined VIRTUAL_ENV (
    deactivate
)

@echo on