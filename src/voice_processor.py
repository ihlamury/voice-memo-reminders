"""
Voice Processor - Handles Claude API interaction for transcription categorization
"""
from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

class VoiceProcessor:
    def __init__(self):
        """Initialize Claude API client"""
        api_key = os.getenv('CLAUDE_API_KEY')
        if not api_key:
            raise ValueError("CLAUDE_API_KEY not found in environment variables")
        self.client = Anthropic(api_key=api_key)
        
    def process_transcription(self, transcription_text):
        """
        Send transcription to Claude for categorization
        
        Args:
            transcription_text (str): The transcribed voice memo text
            
        Returns:
            dict: Categorized tasks with metadata
        """
        prompt = f"""
        Analyze this voice memo transcription and extract actionable tasks.
        For each task, identify:
        - The task description (clear, concise)
        - Priority (high, medium, low, urgent)
        - Category from this list:
        * work - professional tasks, meetings, projects
        * personal - personal errands, self-care, appointments
        * shopping - groceries, purchases, retail
        * health - medical appointments, fitness, wellness
        * finance - bills, banking, investments
        * home - household chores, maintenance, repairs
        * family - family-related tasks, holidays
        * social - events, gatherings, friends
        * learning - courses, reading, skill development
        * calls - phone calls, video calls
        * emails - email-related tasks
        * travel - trips, bookings, transportation
        * other - anything that doesn't fit above categories
        - Due date/time if mentioned (preserve exact phrasing like "tomorrow", "Friday at 2pm", "next week")

        Use context clues to infer the correct category. Examples:
        - "buy milk" → shopping
        - "pay electricity bill" → finance
        - "call doctor" → health
        - "fix leaky faucet" → home
        - "birthday party for Sarah" → social
        - "gym session" → health
        - "quarterly review meeting" → work
        - "read that book" → learning

        Transcription:
        {transcription_text}

        Return the results in JSON format like this:
        {{
            "tasks": [
                {{
                    "description": "task description",
                    "priority": "medium",
                    "category": "category_name",
                    "due_date": "tomorrow" or null
                }}
            ]
        }}
        """
        
        # Call Claude API
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract and parse response
        response_text = message.content[0].text
        
        # Try to parse JSON from response
        try:
            # Find JSON in the response (Claude might add explanation text)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing Claude response: {e}")
            print(f"Raw response: {response_text}")
            return {"tasks": []}

if __name__ == "__main__":
    # Test the processor
    processor = VoiceProcessor()
    test_text = "Remind me to buy milk tomorrow and call John on Monday"
    result = processor.process_transcription(test_text)
    print(json.dumps(result, indent=2))
