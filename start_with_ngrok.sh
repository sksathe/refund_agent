#!/bin/bash
# Start RRVA MCP Server with ngrok
# This script starts both the MCP server and ngrok

echo "========================================"
echo "RRVA MCP Server - ngrok Setup"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

# Check if ngrok is available
if ! command -v ngrok &> /dev/null; then
    echo "ERROR: ngrok is not installed"
    echo "Please install ngrok from https://ngrok.com/download"
    exit 1
fi

# Navigate to project directory
cd "$(dirname "$0")"

echo "[1/2] Starting MCP HTTP Server..."
python3 mcp_server_http.py &
SERVER_PID=$!

# Wait for server to start
sleep 3

echo "[2/2] Starting ngrok tunnel..."
echo ""
echo "IMPORTANT: Keep this terminal open!"
echo ""
echo "Your ngrok URL will be displayed below."
echo "Copy it and use it in ElevenLabs configuration."
echo ""
echo "Press Ctrl+C to stop (server will keep running)"
echo ""

# Start ngrok
ngrok http 8000

# Cleanup on exit
kill $SERVER_PID 2>/dev/null

