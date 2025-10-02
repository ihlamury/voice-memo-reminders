# Voice Memo to Calendar Automation

Apple Watch voice memo processing with AI for intelligent task categorization and Google Calendar integration.

## Overview

Record voice memos on your Apple Watch, and automatically convert them into organized calendar events using AI. The system transcribes your voice, categorizes tasks, extracts due dates, and creates calendar events.

## Project Structure
voice-memo-reminders/
├── src/
│   ├── audio_transcriber.py  # Whisper API for audio transcription
│   ├── voice_processor.py     # Claude API for task categorization
│   └── reminder_manager.py    # Output formatting
├── process_file.py            # File-based processing (text input)
├── process_icloud.py          # iCloud Drive integration (audio input)
├── main.py                    # Simple test script
└── requirements.txt           # Python dependencies

## Current Workflow

1. **Record**: Voice memo on Apple Watch using Voice Memos app (built-in, free)
2. **Transfer**: Voice memo syncs to Mac via iCloud Drive
3. **Transcribe**: Python script uses Whisper API to convert audio to text
4. **Analyze**: Claude AI extracts tasks, priorities, categories, and due dates
5. **Create**: Calendar events generated (Google Calendar integration coming soon)

## Features

- 🎙️ Works with native Voice Memos app (no paid apps required)
- 🤖 AI-powered task categorization using Claude
- 📝 Automatic transcription with OpenAI Whisper
- 📂 Automatic organization by category (work, personal, shopping, health, etc.)
- ⭐ Priority detection (high, medium, low)
- 📅 Due date extraction from natural language
- 🔄 Watch mode for automatic processing
- ☁️ iCloud Drive sync between devices

## Setup

### 1. Clone and Install
```bash
git clone git@github.com:ihlamury/voice-memo-reminders.git
cd voice-memo-reminders
pip install -r requirements.txt

### 2. Configure API Keys
Create a .env file with your API keys:
CLAUDE_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

### 3. Set Up iCloud Drive Folders
The script automatically creates these folders:
Input: ~/Library/Mobile Documents/com~apple~CloudDocs/VoiceMemos/input/
Output: ~/Library/Mobile Documents/com~apple~CloudDocs/VoiceMemos/output/