# ConfNote

Built for **GDG DevFest Toronto 2026** — the challenge was to build something that solves an annoyance from the event.

At fast-paced conference talks, it's easy to miss details, get lost on unfamiliar terms, or forget what you wanted to look up later. **ConfNote** listens to the talk while you focus on jotting down timestamped keywords of topics you care about, then uses the **Gemma 4 API** to compile a clean, tailored study guide around those keywords.

## Features
- **Audio Recording & Live Transcript**: Captures talk audio (`MediaRecorder`) and live speech-to-text (`SpeechRecognition`), plus a **Load Demo Talk** button for quick testing.
- **Timestamped Keyword Logger**: Type any topic or term you want explained or saved and press `Enter`.
- **Gemma 4 Note Compiler**: Summarizes what the speaker covered, explains unfamiliar concepts in plain English, and lists key takeaways (`gemma-4-31b-it`, `gemma-4-26b-a4b-it`, or `gemma-4-4b-it` with native audio).

## Quick Start

1. Copy the example environment file and add your Gemini API key:
   ```bash
   cp .env.example .env
   ```
   Edit `.env`:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

2. Start the local server (Python 3, no extra packages required):
   ```bash
   python3 server.py
   ```

3. Open **http://localhost:8000** in Chrome or Edge.
