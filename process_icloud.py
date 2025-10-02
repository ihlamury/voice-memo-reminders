"""
iCloud Drive-based voice memo processor
Monitors iCloud Drive for new audio files from Voice Memos and processes them
Works with native Voice Memos app - no paid apps required
"""
from src.audio_transcriber import AudioTranscriber
from src.voice_processor import VoiceProcessor
from src.reminder_manager import ReminderManager
from src.calendar_manager import CalendarManager
import os
import json
import time
from pathlib import Path
from datetime import datetime

# iCloud Drive paths - now looking for audio files
ICLOUD_BASE = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/VoiceMemos")
INPUT_FOLDER = os.path.join(ICLOUD_BASE, "input")
OUTPUT_FOLDER = os.path.join(ICLOUD_BASE, "output")

def ensure_folders_exist():
    """Create iCloud folders if they don't exist"""
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    print(f"✅ Folders ready:")
    print(f"   Input:  {INPUT_FOLDER}")
    print(f"   Output: {OUTPUT_FOLDER}")

def process_audio_file(audio_path):
    """
    Process a voice memo audio file
    
    Args:
        audio_path (str): Path to audio file
        
    Returns:
        str: Path to output file, or None if failed
    """
    try:
        print(f"\n🎙️  Processing: {os.path.basename(audio_path)}")
        
        # Step 1: Transcribe audio
        print("📝 Transcribing audio with Whisper...")
        transcriber = AudioTranscriber()
        transcription = transcriber.transcribe_audio(audio_path)
        
        if not transcription:
            print("⚠️  Transcription failed, skipping...")
            return None
        
        print(f"   Transcription length: {len(transcription)} characters")
        print(f"   Preview: {transcription[:100]}...")
        
        # Step 2: Process with Claude
        print("🤖 Processing with Claude...")
        voice_processor = VoiceProcessor()
        categorized_tasks = voice_processor.process_transcription(transcription)
        
        # Step 3: Format output
        print("📝 Formatting results...")
        reminder_manager = ReminderManager()
        formatted_results = reminder_manager.format_reminders(categorized_tasks)
        
        # Step 4: Create Google Calendar events
        print("📅 Creating calendar events...")
        from src.calendar_manager import CalendarManager
        calendar_manager = CalendarManager()
        calendar_manager.create_events_from_json(formatted_results)
        
        # Step 5: Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        input_basename = os.path.splitext(os.path.basename(audio_path))[0]
        output_filename = f"{input_basename}_processed_{timestamp}.json"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_results)
        
        print(f"✅ Results saved: {os.path.basename(output_path)}")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Error processing {audio_path}: {e}")
        import traceback
        traceback.print_exc()
        return None

def process_all_pending():
    """Process all audio files currently in the input folder"""
    ensure_folders_exist()
    
    # Get all audio files - Voice Memos typically use .m4a
    audio_extensions = ['*.m4a', '*.mp3', '*.wav', '*.m4v']
    input_files = []
    
    for ext in audio_extensions:
        input_files.extend(list(Path(INPUT_FOLDER).glob(ext)))
    
    if not input_files:
        print("\n📭 No audio files to process in input folder")
        return
    
    print(f"\n📬 Found {len(input_files)} audio file(s) to process")
    
    for audio_file in input_files:
        process_audio_file(str(audio_file))
        print()  # Blank line between files
    
    print("🎉 All files processed!")

def watch_mode(check_interval=30):
    """
    Watch mode - continuously monitor input folder for new audio files
    
    Args:
        check_interval (int): Seconds between checks (30s default for audio files)
    """
    ensure_folders_exist()
    
    print(f"\n👀 Watch mode started - checking every {check_interval} seconds")
    print("   Monitoring for: .m4a, .mp3, .wav files")
    print("   Press Ctrl+C to stop\n")
    
    processed_files = set()
    audio_extensions = ['*.m4a', '*.mp3', '*.wav', '*.m4v']
    
    try:
        while True:
            # Get current audio files
            current_files = set()
            for ext in audio_extensions:
                current_files.update(Path(INPUT_FOLDER).glob(ext))
            
            # Find new files
            new_files = current_files - processed_files
            
            if new_files:
                print(f"📬 Found {len(new_files)} new audio file(s)!")
                for new_file in new_files:
                    process_audio_file(str(new_file))
                    processed_files.add(new_file)
                    print()
            
            # Wait before next check
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        print("\n\n👋 Watch mode stopped")

def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "watch":
        # Watch mode - continuous monitoring
        watch_mode()
    else:
        # Process all pending files once
        process_all_pending()

if __name__ == "__main__":
    main()