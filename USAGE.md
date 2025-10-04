# Usage Guide

## Daily Workflow

1. Record voice memo on Apple Watch
2. Manually move .m4a file to iCloud Drive/VoiceMemos/input/
3. Mac runs: `python process_icloud.py watch`
4. Check Google Calendar for scheduled tasks

## Tips

- Speak clearly and mention dates/times
- Include priority keywords: "urgent", "important"
- Categories are auto-detected from context
- Tasks without times start at 9 AM and stagger automatically

## Troubleshooting

- **Transcription in wrong language**: Check audio_transcriber.py language setting
- **Calendar events at wrong time**: Check timezone in calendar_manager.py
- **API errors**: Check .env file has valid keys

## Cost Tracking

- Whisper: ~$0.006 per minute of audio
- Claude: Pay-per-use
- Google Calendar: Free