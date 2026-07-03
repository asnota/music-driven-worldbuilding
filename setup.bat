@echo off
setlocal EnableDelayedExpansion

REM ============================================================
REM  Music-Driven Worldbuilding - Setup Script
REM  (Run this from the repo root)
REM ============================================================

REM Always work relative to where THIS script lives
cd /d "%~dp0"

set "PROJECT_SUBDIR=flask-app"

echo.
echo ============================================================
echo  [1/5] Locating project folder...
echo ============================================================
if exist "%PROJECT_SUBDIR%\pyproject.toml" (
    cd "%PROJECT_SUBDIR%" || goto :error
    echo Found project in "%PROJECT_SUBDIR%".
) else if exist "pyproject.toml" (
    echo Found project in repo root.
) else (
    echo ERROR: Could not find pyproject.toml in repo root or "%PROJECT_SUBDIR%".
    goto :error
)

echo.
echo ============================================================
echo  [2/5] Installing uv...
echo ============================================================
where uv >nul 2>&1
if %errorlevel%==0 (
    echo uv is already installed.
) else (
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" || goto :error
)

REM uv installs to %USERPROFILE%\.local\bin - add it to PATH for THIS session
set "PATH=%USERPROFILE%\.local\bin;%PATH%"

where uv >nul 2>&1 || (
    echo ERROR: uv not found on PATH after install.
    echo Close this window, open a NEW terminal, then re-run.
    goto :error
)

echo.
echo ============================================================
echo  [3/5] Installing and pinning Python 3.11...
echo ============================================================
uv python install 3.11 || goto :error
uv python pin 3.11     || goto :error

echo.
echo ============================================================
echo  [4/5] Syncing dependencies from pyproject.toml...
echo ============================================================
REM Creates .venv (if missing) and installs everything in pyproject.toml
uv sync || goto :error

echo.
echo ============================================================
echo  [5/5] Installing PyTorch (CUDA build) + training utils...
echo ============================================================
REM These are NOT in pyproject.toml and must be installed separately
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128 || goto :error
uv pip install tensorboardX pytorch_lightning || goto :error

echo.
echo ============================================================
echo  Setup complete!
echo ============================================================
echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo ------------------------------------------------------------
echo  Environment is ready and ACTIVATED.
echo.
echo  To start the Flask app, run:
echo      uv run app.py
echo.
echo  The service will be available at port 500 (or 5000).
echo  Panoramas  -^> generated_panorama_web
echo  Music      -^> generated_music
echo ------------------------------------------------------------
echo.

REM Keep the activated shell open so the user can run commands
cmd /k

goto :eof

:error
echo.
echo ############################################################
echo  ERROR: A step failed (exit code %errorlevel%).
echo  Setup aborted.
echo ############################################################
pause
exit /b 1