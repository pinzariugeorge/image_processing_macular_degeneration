@ECHO OFF

set venv_path=%~dp0\venv

REM Check if virtual environment exists
if not exist %venv_path% (
    call %~dp0\create_venv.bat
)

REM Activate virtual environment
call %venv_path%\Scripts\activate.bat

REM Upgrade pip
python main.py

call %venv_path%\Scripts\deactivate.bat



