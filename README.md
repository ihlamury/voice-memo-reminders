# Voice Memo to Reminders Automation

Apple Watch voice memo processing with Claude AI for intelligent task categorization and iOS Reminders integration.

## Overview

Record voice memos on your Apple Watch, and automatically convert them into organized reminders using AI. The system transcribes your voice, categorizes tasks, and adds them to your iOS Reminders app.

## Project Structure
voice-memo-reminders/
├── src/
│   ├── voice_processor.py    # Claude API integration & categorization
│   └── reminder_manager.py   # Format output for iOS Shortcuts
├── main.py                   # Simple test script
├── process_file.py           # File-based processing
├── process_icloud.py         # iCloud Drive integration with watch mode
└── requirements.txt          # Python dependencies

## Workflow

1. **Record**: Voice memo on Apple Watch using Voice Memos app (built-in, free)
2. **Transcribe**: iOS Shortcuts uses built-in speech recognition to create text
3. **Save**: iOS Shortcuts saves transcription to iCloud Drive
4. **Process**: Python script sends transcription to Claude for categorization
5. **Format**: Structures data with categories, priorities, and due dates
6. **Create**: iOS Shortcuts reads results and adds to Reminders app

## Features

- 🎙️ Works with native Voice Memos app (no paid apps required)
- 🤖 AI-powered task categorization using Claude
- 📂 Automatic organization by category (work, personal, shopping, health, etc.)
- ⭐ Priority detection (high, medium, low)
- 📅 Due date extraction from natural language
- 🔄 Automatic processing with watch mode
- ☁️ iCloud Drive sync between devices

## Setup

### 1. Clone and Install
```bash
git clone git@github.com:ihlamury/voice-memo-reminders.git
cd voice-memo-reminders
pip install -r requirements.txt


### 2. Configure API Key

CLAUDE_API_KEY=your_anthropic_api_key_here

### 3. Test the System
# Test with sample file
python process_file.py

# Test with iCloud Drive
python process_icloud.py

# Run in watch mode for automatic processing
python process_icloud.py watch