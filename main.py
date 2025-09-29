"""
Main entry point for voice memo processing
"""
from src.voice_processor import VoiceProcessor
from src.reminder_manager import ReminderManager
import sys

def main():
    """
    Process voice memo and create reminders
    """
    # For now, just test with sample text
    sample_transcription = """
    I need to buy groceries tomorrow - milk, eggs, and bread.
    Also remind me to call the dentist on Monday to schedule an appointment.
    """
    
    # Initialize processors
    voice_processor = VoiceProcessor()
    reminder_manager = ReminderManager()
    
    # Process transcription with Claude
    print("Processing voice memo...")
    categorized_tasks = voice_processor.process_transcription(sample_transcription)
    
    # Format for reminders
    print("\nFormatting reminders...")
    formatted_reminders = reminder_manager.format_reminders(categorized_tasks)
    
    # Display results
    print("\nReminders created:")
    print(formatted_reminders)

if __name__ == "__main__":
    main()
