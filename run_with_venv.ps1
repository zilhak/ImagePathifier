# ImagePathifier Run Script with venv

# Create venv if not exists
if (-not (Test-Path venv)) {
    Write-Host "Virtual environment not found. Setting up..." -ForegroundColor Yellow
    .\setup_venv.ps1
}

# Activate and run
& .\venv\Scripts\Activate.ps1
python ImagePathifier.py