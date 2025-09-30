"""
iCloud Drive-based voice memo processor
Monitors iCloud Drive for new transcriptions and processes them automatically
"""
from src.voice_processor import VoiceProcessor
from src.reminder_manager import ReminderManager
import os
import json
import time
from pathlib import Path
from datetime import datetime

# iCloud Drive paths
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

def process_file(input_path):
    """
    Process a single transcription file
    
    Args:
        input_path (str): Path to input transcription file
        
    Returns:
        str: Path to output file, or None if failed
    """
    try:
        # Read transcription
        print(f"\n📖 Reading: {os.path.basename(input_path)}")
        with open(input_path, 'r', encoding='utf-8') as f:
            transcription = f.read().strip()
        
        if not transcription:
            print("⚠️  File is empty, skipping...")
            return None
        
        print(f"   Length: {len(transcription)} characters")
        
        # Initialize processors
        voice_processor = VoiceProcessor()
        reminder_manager = ReminderManager()
        
        # Process with Claude
        print("🤖 Processing with Claude...")
        categorized_tasks = voice_processor.process_transcription(transcription)
        
        # Format reminders
        print("📝 Formatting reminders...")
        formatted_reminders = reminder_manager.format_reminders(categorized_tasks)
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        input_basename = os.path.splitext(os.path.basename(input_path))[0]
        output_filename = f"{input_basename}_reminders_{timestamp}.json"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_reminders)
        
        print(f"✅ Results written to: {os.path.basename(output_path)}")
        
        # Optionally, move processed input to archive or delete
        # os.remove(input_path)  # Uncomment to auto-delete after processing
        
        return output_path
        
    except Exception as e:
        print(f"❌ Error processing {input_path}: {e}")
        return None

def process_all_pending():
    """Process all files currently in the input folder"""
    ensure_folders_exist()
    
    # Get all .txt files in input folder
    input_files = list(Path(INPUT_FOLDER).glob("*.txt"))
    
    if not input_files:
        print("\n📭 No files to process in input folder")
        return
    
    print(f"\n📬 Found {len(input_files)} file(s) to process")
    
    for input_file in input_files:
        process_file(str(input_file))
        print()  # Blank line between files
    
    print("🎉 All files processed!")

def watch_mode(check_interval=10):
    """
    Watch mode - continuously monitor input folder for new files
    
    Args:
        check_interval (int): Seconds between checks
    """
    ensure_folders_exist()
    
    print(f"\n👀 Watch mode started - checking every {check_interval} seconds")
    print("   Press Ctrl+C to stop\n")
    
    processed_files = set()
    
    try:
        while True:
            # Get current files
            current_files = set(Path(INPUT_FOLDER).glob("*.txt"))
            
            # Find new files
            new_files = current_files - processed_files
            
            if new_files:
                print(f"📬 Found {len(new_files)} new file(s)!")
                for new_file in new_files:
                    process_file(str(new_file))
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