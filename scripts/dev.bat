@echo off
:: Development helper script for TaskbarManager
:: Usage: scripts\dev.bat [command]

if "%1"=="setup" goto setup
if "%1"=="run" goto run
if "%1"=="test" goto test
if "%1"=="lint" goto lint
if "%1"=="format" goto format
if "%1"=="build" goto build
if "%1"=="clean" goto clean
if "%1"=="" goto help
goto help

:setup
echo Setting up development environment...
python -m venv .venv
call .venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements-dev.txt
echo Setup complete! Run 'scripts\dev.bat run' to start the application.
goto end

:run
echo Starting TaskbarManager...
call .venv\Scripts\activate.bat
python src\taskbar_manager.py
goto end

:test
echo Running tests...
call .venv\Scripts\activate.bat
pytest tests/ -v --cov=src --cov-report=html
goto end

:lint
echo Running linting...
call .venv\Scripts\activate.bat
flake8 src/
mypy src/
goto end

:format
echo Formatting code...
call .venv\Scripts\activate.bat
black src/
isort src/
echo Code formatted successfully.
goto end

:build
echo Building executable...
call .venv\Scripts\activate.bat
python build.py
echo Build complete! Check the dist/ folder.
goto end

:clean
echo Cleaning build artifacts...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
rmdir /s /q *.egg-info 2>nul
rmdir /s /q __pycache__ 2>nul
rmdir /s /q .pytest_cache 2>nul
rmdir /s /q .mypy_cache 2>nul
rmdir /s /q htmlcov 2>nul
del /q *.pyc 2>nul
echo Clean complete.
goto end

:help
echo TaskbarManager Development Helper
echo.
echo Usage: scripts\dev.bat [command]
echo.
echo Available commands:
echo   setup   - Set up development environment
echo   run     - Run the application
echo   test    - Run tests with coverage
echo   lint    - Run linting (flake8, mypy)
echo   format  - Format code (black, isort)
echo   build   - Build executable
echo   clean   - Clean build artifacts
echo   help    - Show this help message
echo.

:end