# Reversi Game Launcher - PowerShell Version
param(
    [string]$Version = "advanced"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "           REVERSI GAME LAUNCHER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.6+ from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pygame is installed
try {
    python -c "import pygame" 2>$null
    Write-Host "Pygame found. Dependencies OK!" -ForegroundColor Green
} catch {
    Write-Host "Installing pygame..." -ForegroundColor Yellow
    try {
        pip install pygame
        Write-Host "Pygame installed successfully!" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to install pygame" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""

# Choose game version if not specified
if ($Version -eq "advanced") {
    $gameFile = "reversi_advanced.py"
    Write-Host "Starting Advanced Reversi (Full Menu + Advanced AI)..." -ForegroundColor Green
} elseif ($Version -eq "basic") {
    $gameFile = "reversi_pygame.py"
    Write-Host "Starting Basic Reversi (Simple AI)..." -ForegroundColor Green
} else {
    Write-Host "Choose game version:" -ForegroundColor White
    Write-Host "1. Basic Reversi (Simple AI)" -ForegroundColor White
    Write-Host "2. Advanced Reversi (Full Menu + Advanced AI) - RECOMMENDED" -ForegroundColor White
    Write-Host ""
    
    $choice = Read-Host "Enter your choice (1-2)"
    
    if ($choice -eq "1") {
        $gameFile = "reversi_pygame.py"
        Write-Host "Starting Basic Reversi..." -ForegroundColor Green
    } elseif ($choice -eq "2") {
        $gameFile = "reversi_advanced.py"
        Write-Host "Starting Advanced Reversi..." -ForegroundColor Green
    } else {
        Write-Host "Invalid choice. Exiting..." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# Check if game file exists
if (-not (Test-Path $gameFile)) {
    Write-Host "ERROR: Game file '$gameFile' not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Launch the game
try {
    python $gameFile
} catch {
    Write-Host "ERROR: Failed to start the game" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host ""
Write-Host "Game finished. Press Enter to exit..." -ForegroundColor Yellow
Read-Host 