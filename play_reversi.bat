@echo off
title Reversi Game

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://python.org
    pause
    exit /b 1
)

REM Check if pygame is installed and install if needed
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo Installing pygame...
    pip install pygame
)

REM Launch the advanced Reversi game
python reversi_advanced.py 