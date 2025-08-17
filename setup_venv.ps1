# ImagePathifier Virtual Environment Setup Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ImagePathifier Virtual Environment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Python version:" -ForegroundColor Yellow
py --version
Write-Host ""

# Remove existing venv if exists
if (Test-Path venv) {
    Write-Host "Removing existing virtual environment..." -ForegroundColor Yellow
    Remove-Item venv -Recurse -Force
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
py -m venv venv
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install packages
Write-Host "Installing required packages..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To run the program:" -ForegroundColor Cyan
Write-Host "  1. .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  2. python ImagePathifier.py" -ForegroundColor White
Write-Host ""
Write-Host "Or just run: .\run_with_venv.ps1" -ForegroundColor Yellow
Write-Host "========================================"