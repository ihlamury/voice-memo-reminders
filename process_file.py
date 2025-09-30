"""
File-based voice memo processor
Reads transcription from input file, processes with Claude, writes results to output file
"""
from src.voice_processor import VoiceProcessor
from src.reminder_manager import ReminderManager
import sys
import json
import os
from pathlib import Path

def process_transcription_file(input_file, output_file):
    """
    Process a transcription file and create reminders output
    
    Args:
        input_file (str): Path to input transcription file
        output_file (str): Path to output reminders file
    """
    try:
        # Read input file
        print(f"Reading transcription from: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            transcription = f.read().strip()
        
        if not transcription:
            print("Error: Input file is empty")
            return False
        
        print(f"Transcription length: {len(transcription)} characters")
        
        # Initialize processors
        voice_processor = VoiceProcessor()
        reminder_manager = ReminderManager()
        
        # Process with Claude
        print("Processing with Claude...")
        categorized_tasks = voice_processor.process_transcription(transcription)
        
        # Format reminders
        print("Formatting reminders...")
        formatted_reminders = reminder_manager.format_reminders(categorized_tasks)
        
        # Write output file
        print(f"Writing results to: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(formatted_reminders)
        
        print("✅ Processing complete!")
        print(f"\nResults preview:")
        print(formatted_reminders)
        
        return True
        
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_file}")
        return False
    except Exception as e:
        print(f"Error processing file: {e}")
        return False

def main():
    """
    Main entry point - supports command line arguments or defaults
    """
    if len(sys.argv) == 3:
        # Use command line arguments
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        # Use default test files
        input_file = "test_input.txt"
        output_file = "test_output.json"
        print(f"Usage: python process_file.py <input_file> <output_file>")
        print(f"Using defaults: {input_file} -> {output_file}\n")
    
    # Process the file
    success = process_transcription_file(input_file, output_file)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()