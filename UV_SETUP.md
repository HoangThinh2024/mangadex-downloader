# Setup and Run Guide for uv (Astral Python)

## Prerequisites
- Python 3.11+ 
- uv installed (https://docs.astral.sh/uv/getting-started/)

## Installation

### Option 1: Using uv sync (Recommended)
```powershell
# Navigate to project
cd C:\mangadex-downloader

# Create virtual environment and install dependencies
uv sync

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

### Option 2: Using uv pip directly
```powershell
cd C:\mangadex-downloader

# Create venv
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install with uv
uv pip install -e .
```

### Option 3: Install from requirements
```powershell
cd C:\mangadex-downloader

# Install directly
uv pip install -r requirements-uv.txt
```

## Running the Web App

After installation, run:

```powershell
uv run python run_web.py
```

Or if you activated venv:
```powershell
python run_web.py
```

## Verifying Installation

```powershell
# Check all imports work
uv run python -c "import fastapi; import mangadex_downloader; print('✓ All dependencies installed')"

# Check web app can start
uv run python run_web.py
```

## With uv sync

The `pyproject.toml` file allows modern dependency management:

```powershell
# Sync dependencies (creates .venv)
uv sync

# Activate venv
.\.venv\Scripts\Activate.ps1

# Run
python run_web.py
```

## Troubleshooting

### If uv is not installed:
```powershell
pip install uv
# or
curl -LsSf https://astral.sh/uv/install.ps1 | powershell -c -
```

### If port 8000 is in use:
Edit `run_web.py`, change `port=8000` to `port=8001`

### If dependencies fail:
```powershell
# Try with --upgrade
uv pip install --upgrade -r requirements-uv.txt

# Or clean and reinstall
uv sync --fresh
```

## Web App Access

Once running:
- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Search**: http://localhost:8000/api/search/manga?q=one+piece

## Using uv to run scripts

You can also use uv to run Python commands without activating venv:

```powershell
# Run web app
uv run python run_web.py

# Run Python scripts
uv run python some_script.py

# Run with custom interpreter
uv run --python 3.11 python run_web.py
```

## uv Commands Reference

```powershell
# Create/update lock file
uv lock --upgrade

# Sync environment
uv sync

# Install package
uv pip install package_name

# Install from file
uv pip install -r requirements.txt

# Run in uv environment
uv run python script.py

# List installed packages
uv pip list

# Remove package
uv pip uninstall package_name
```

## Next Steps

1. Follow installation steps above
2. Run `python run_web.py` (or `uv run python run_web.py`)
3. Open http://localhost:8000
4. Search for manga, queue downloads, monitor progress

## Documentation

- `WEBAPP_README.md` - Full API documentation
- `SETUP_GUIDE.txt` - Quick start guide
- `COMPLETE_SOURCE.txt` - All source code
- `README_WEBAPP.txt` - Feature overview
