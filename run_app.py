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
    frontend_path = (Path(__file__).resolve().parent / "frontend" / "index.html").as_uri()
    print("=" * 65)
    print(" VoiceCoach Indic - Language Coach with Your Own Voice")
    print(" Powered by Sarvam AI Indic Speech Models")
    print("=" * 65)
    print(f"[*] Backend API: http://localhost:{settings.APP_PORT}/docs")
    print(f"[*] Frontend Studio: {frontend_path}")
    print("[*] Sarvam API Key: Loaded and configured.")
    print("=" * 65)
    print("Opening web interface in your browser...")
    webbrowser.open(frontend_path)
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.APP_PORT, reload=True, app_dir=str(backend_dir))

