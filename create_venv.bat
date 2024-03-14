@ECHO OFF

set venv_path=%~dp0\venv

REM Check if virtual environment exists
if not exist %venv_path% (
    echo Creating virtual environment...
    python -m venv %venv_path%
	REM Activate virtual environment
	call %venv_path%\Scripts\activate.bat

	REM Upgrade pip
	python -m pip install --upgrade pip

	REM Install dependencies
	python -m pip install -r requirements.txt

	echo Virtual environment setup complete.
	call %venv_path%\Scripts\deactivate.bat
)





