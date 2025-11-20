@echo off
REM Start RRVA MCP Server with ngrok
REM This script starts both the MCP server and ngrok

echo ========================================
echo RRVA MCP Server - ngrok Setup
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if ngrok is available
ngrok version >nul 2>&1
if errorlevel 1 (
    echo ERROR: ngrok is not installed or not in PATH
    echo Please install ngrok from https://ngrok.com/download
    pause
    exit /b 1
)

REM Navigate to project directory
cd /d "%~dp0"

echo [1/2] Starting MCP HTTP Server...
start "RRVA MCP Server" cmd /k "python mcp_server_http.py"

REM Wait a moment for server to start
timeout /t 3 /nobreak >nul

echo [2/2] Starting ngrok tunnel...
echo.
echo IMPORTANT: Keep both windows open!
echo.
echo Your ngrok URL will be displayed below.
echo Copy it and use it in ElevenLabs configuration.
echo.
echo Press Ctrl+C to stop ngrok (server will keep running)
echo.

ngrok http 8000

pause

