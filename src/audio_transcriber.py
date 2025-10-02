"""
Audio Transcriber - Handles audio file transcription using OpenAI Whisper
"""
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class AudioTranscriber:
    def __init__(self):
        """Initialize OpenAI client"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
    
    def transcribe_audio(self, audio_file_path):
        """
        Transcribe an audio file to text using Whisper API
        
        Args:
            audio_file_path (str): Path to audio file (.m4a, .mp3, .wav, etc.)
            
        Returns:
            str: Transcribed text
        """
        try:
            # Open audio file
            with open(audio_file_path, 'rb') as audio_file:
                # Call Whisper API
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text",
                    language="en"  # Force English transcription
                )
            
            return transcript.strip()
            
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None

if __name__ == "__main__":
    # Test the transcriber
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python src/audio_transcriber.py <audio_file_path>")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    
    if not os.path.exists(audio_path):
        print(f"Error: File not found: {audio_path}")
        sys.exit(1)
    
    print(f"Transcribing: {audio_path}")
    transcriber = AudioTranscriber()
    result = transcriber.transcribe_audio(audio_path)
    
    if result:
        print(f"\nTranscription:\n{result}")
    else:
        print("Transcription failed")