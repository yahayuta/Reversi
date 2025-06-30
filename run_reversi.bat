@echo off
title Reversi Game Launcher

echo ========================================
echo           REVERSI GAME LAUNCHER
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Checking dependencies...

REM Check if pygame is installed
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo Installing pygame...
    pip install pygame
    if errorlevel 1 (
        echo ERROR: Failed to install pygame
        pause
        exit /b 1
    )
)

echo.
echo Dependencies OK!
echo.
echo Choose game version:
echo 1. Basic Reversi (Simple AI)
echo 2. Advanced Reversi (Full Menu + Advanced AI) - RECOMMENDED
echo 3. Exit
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Starting Basic Reversi...
    python reversi_pygame.py
) else if "%choice%"=="2" (
    echo.
    echo Starting Advanced Reversi...
    python reversi_advanced.py
) else if "%choice%"=="3" (
    echo.
    echo Goodbye!
    exit /b 0
) else (
    echo.
    echo Invalid choice. Please run the batch file again.
    pause
    exit /b 1
)

echo.
echo Game finished. Press any key to exit...
pause >nul 