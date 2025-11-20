# Quick Start with ngrok

Get your MCP server exposed to ElevenLabs in 3 steps.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs FastAPI and uvicorn for the HTTP server.

## Step 2: Start Server & ngrok

### Windows

Double-click `start_with_ngrok.bat` or run:

```bash
start_with_ngrok.bat
```

### Mac/Linux

```bash
chmod +x start_with_ngrok.sh
./start_with_ngrok.sh
```

### Manual Start

**Terminal 1 - Start MCP Server:**
```bash
python mcp_server_http.py
```

**Terminal 2 - Start ngrok:**
```bash
ngrok http 8000
```

## Step 3: Configure ElevenLabs

1. Copy your ngrok URL (e.g., `https://abc123.ngrok-free.app`)
2. In ElevenLabs dashboard:
   - Add MCP Server
   - Transport: `https`
   - Server URL: `https://abc123.ngrok-free.app`
   - Endpoint: `/mcp`

Done! Your tools are now available to ElevenLabs.

## Test It

Visit in browser:
- `https://your-url.ngrok-free.app/health`
- `https://your-url.ngrok-free.app/tools`

## Troubleshooting

**Server not starting?**
- Check Python: `python --version`
- Install deps: `pip install -r requirements.txt`

**ngrok not working?**
- Authenticate: `ngrok authtoken YOUR_TOKEN`
- Check port: Server must be on port 8000

**Tools not discovered?**
- Test: `https://your-url.ngrok-free.app/tools`
- Check ElevenLabs endpoint configuration

---

**Full guide:** See `NGROK_SETUP.md` for detailed instructions.

