#!/usr/bin/env powershell
# Install MangaDex Downloader Web App using uv

Write-Host "Installing MangaDex Downloader Web App..." -ForegroundColor Green

# Check if uv is installed
$uvExists = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uvExists) {
    Write-Host "uv not found. Installing uv..." -ForegroundColor Yellow
    pip install uv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install uv" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✓ uv is installed" -ForegroundColor Green

# Option 1: Using uv sync (creates .venv)
Write-Host "`nInstalling dependencies with uv sync..." -ForegroundColor Cyan
uv sync

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to sync with uv" -ForegroundColor Red
    
    # Fallback to uv pip install
    Write-Host "`nFalling back to uv pip install..." -ForegroundColor Yellow
    uv pip install -e .
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n✓ Dependencies installed" -ForegroundColor Green

# Test imports
Write-Host "`nTesting imports..." -ForegroundColor Cyan
uv run python -c "import fastapi; import mangadex_downloader; print('✓ All imports successful')" 

if ($LASTEXITCODE -ne 0) {
    Write-Host "Import test failed" -ForegroundColor Red
    exit 1
}

Write-Host "`n✓ Installation complete!" -ForegroundColor Green
Write-Host "`nTo run the web app:" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\Activate.ps1   # Activate venv" -ForegroundColor White
Write-Host "  python .\run_web.py             # Run server" -ForegroundColor White
Write-Host "`nOr use uv directly:" -ForegroundColor Cyan
Write-Host "  uv run python .\run_web.py      # Run without activating" -ForegroundColor White
Write-Host "`nThen open: http://localhost:8000" -ForegroundColor Green
