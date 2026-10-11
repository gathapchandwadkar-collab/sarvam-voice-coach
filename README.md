# VoiceCoach Indic - Language Coach with Your Own Voice

> **Clone a learner's voice, then generate correct pronunciation of new vocabulary or phrases in their own voice.**  
> Removes the awkwardness of hearing a stranger's voice while learning — hear yourself speaking correctly across Indian languages.

---

## 🌟 Key Concept

When practicing a new language (Hindi, Tamil, Telugu, Kannada, Marathi, Bengali, etc.), hearing native speakers can often feel intimidating or unnatural to mimic. **VoiceCoach Indic** bridges this gap:
1. **Enroll Voice**: Record a 15-30 second audio sample of the learner speaking any familiar sentence.
2. **Zero-Shot / Few-Shot Voice Profile**: Extract speaker timbre, pitch characteristics, and speaker embeddings.
3. **Target Language Synthesis**: When a learner practices target vocabulary or phrases, speech is synthesized with native phonetic precision and accent, but **rendered in the learner's own voice**.
4. **Pronunciation Feedback**: Compare learner's practice attempts with the gold-standard pronunciation (audio alignment & acoustic scoring).

---

## 📁 Repository Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/       # Endpoints: voice profiles, synthesis, scoring, languages
│   │   ├── core/                    # App configuration, security, environment setup
│   │   ├── services/
│   │   │   ├── voice_clone/         # Speaker embedding extraction & voice cloning engine
│   │   │   ├── indic_nlp/           # Indic phonetics, transliteration & grapheme-to-phoneme
│   │   │   ├── pronunciation_eval/  # ASR, phoneme alignment & pronunciation scoring
│   │   │   └── sarvam_client/       # Sarvam AI API client integration (TTS / ASR)
│   │   ├── models/                  # Pydantic schemas & database models
│   │   └── main.py                  # FastAPI application entrypoint
│   └── requirements.txt
├── frontend/                        # Web interface (Voice recording, practice studio, playback)
│   └── src/
│       ├── components/              # Audio recorder, waveform visualizer, practice cards
│       └── services/                # API communication layer
├── data/
│   ├── vocabulary/                  # Curated phrase banks & vocabulary for Indian languages
│   ├── voice_profiles/              # Stored speaker embeddings & reference samples
│   └── audio_cache/                 # Cached synthesized reference audio
├── docs/                            # Architecture and API documentation
└── scripts/                         # Utility scripts (seed data, test audio)
```

---

## 🚀 Quick Start

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
cp ../.env.example ../.env
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
