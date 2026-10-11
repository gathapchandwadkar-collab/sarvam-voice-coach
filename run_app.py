import os
import sys
import webbrowser
import uvicorn
from pathlib import Path

# Add backend to sys.path
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.main import app
from app.core.config import settings

if __name__ == "__main__":
    server_url = f"http://localhost:{settings.APP_PORT}"
    print("=" * 65)
    print(" VoiceCoach Indic - Language Coach with Your Own Voice")
    print(" Powered by Sarvam AI Indic Speech Models")
    print("=" * 65)
    print(f"[*] Application Studio: {server_url}/")
    print(f"[*] Interactive API Docs: {server_url}/docs")
    print("[*] Sarvam API Key: Loaded and configured.")
    print("=" * 65)
    print("Opening web interface in your browser...")
    webbrowser.open(f"{server_url}/")
    
    uvicorn.run("app.main:app", host="127.0.0.1", port=settings.APP_PORT, reload=False, app_dir=str(backend_dir))

