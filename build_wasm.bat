@echo off
REM Build script for deploying the game to WASM using pygbag (Windows)

echo Building Zelda-Style Game for WASM...
echo =======================================

REM Check if pygbag is installed
where pygbag >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: pygbag is not installed
    echo Please install it with: pip install pygbag
    exit /b 1
)

REM Clean previous build
if exist "build" (
    echo Cleaning previous build...
    rmdir /s /q build
)

REM Build with pygbag
echo Building with pygbag...
pygbag --template noctx.tmpl .

echo.
echo Build complete!
echo ===============
echo.
echo To test locally, run: pygbag --server .
echo Then open http://localhost:8000 in your browser
echo.
echo To deploy to GitHub Pages or itch.io, upload the contents of the 'build\web' directory
