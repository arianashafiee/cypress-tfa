# Cypress TFA

See notion article: https://polar-galette-e56.notion.site/CypressTFA-Triple-Factor-Facial-Auth-Using-Hand-Motions-1c783a3d3138808c87dcfffffefb1175

Triple-factor authentication that verifies users with liveness detection, facial recognition, and hand gestures. A Chrome extension intercepts logins on supported sites and opens a camera-based auth flow backed by a FastAPI server.

## How it works

1. **Liveness** — blocks spoofing with static images or video replays
2. **Face match** — compares the live feed against an enrolled face encoding stored in MongoDB
3. **Gestures** — prompts for three random hand gestures before access is granted

Supported sites: X, GitHub, Instagram, and Incomee.

## Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB Atlas cluster (or compatible MongoDB instance)
- Chrome browser
- Webcam

## Installation

### 1. Clone and configure environment

```bash
git clone https://github.com/arianashafiee/cypress-tfa.git
cd cypress-tfa
cp .env.example .env
```

Set `MONGO_URI` in `.env` to your MongoDB connection string.

### 2. Backend

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Download the [dima806 hand gesture model](https://huggingface.co/dima806/hand_gestures_image_detection) and place it at `backend/CV/gestures/gestures_model/`.

```bash
cd backend
python backend.py
```

The API runs at `http://localhost:8000`.

### 3. Auth UI (Next.js)

```bash
cd frontend/cypress-app
npm install
npm run dev
```

The auth page runs at `http://localhost:3000/auth`.

### 4. Chrome extension

1. Open `chrome://extensions`
2. Enable **Developer mode**
3. Click **Load unpacked** and select `frontend/extension`

## Usage

1. Start the backend and Next.js app
2. Visit a supported site and begin login
3. The extension opens the auth window — allow camera access
4. Complete face verification and the three gesture prompts
5. On success, the original login proceeds

## Tech stack

Python · FastAPI · MongoDB · OpenCV · DeepFace · MediaPipe · Transformers · Next.js · Chrome Extension API
