"""
Calendar Manager - Handles Google Calendar event creation
"""
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from dateutil import parser
import os
import json

# Scopes required for calendar access
SCOPES = ['https://www.googleapis.com/auth/calendar']

class CalendarManager:
    def __init__(self, credentials_path='credentials.json'):
        """Initialize Google Calendar API client"""
        self.credentials_path = credentials_path
        self.service = self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None
        token_path = 'token.json'
        
        # Token stores the user's access and refresh tokens
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        
        return build('calendar', 'v3', credentials=creds)
    
    def parse_natural_date(self, date_string):
        """
        Parse natural language dates like 'tomorrow', 'Friday', 'next week'
        
        Args:
            date_string (str): Natural language date
            
        Returns:
            datetime: Parsed datetime object
        """
        if not date_string:
            # Default to tomorrow at 9 AM if no date specified
            return datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
        
        date_string = date_string.lower().strip()
        now = datetime.now()
        
        # Handle common cases
        if 'tomorrow' in date_string:
            return now.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
        elif 'today' in date_string:
            return now.replace(hour=9, minute=0, second=0, microsecond=0)
        elif 'next week' in date_string:
            return now.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=7)
        
        # Try to parse day of week (Monday, Tuesday, etc.)
        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for i, day in enumerate(days_of_week):
            if day in date_string:
                # Find next occurrence of this day
                current_weekday = now.weekday()
                target_weekday = i
                days_ahead = target_weekday - current_weekday
                if days_ahead <= 0:
                    days_ahead += 7
                return now.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=days_ahead)
        
        # Try general date parsing
        try:
            return parser.parse(date_string, default=now.replace(hour=9, minute=0))
        except:
            # Default to tomorrow if parsing fails
            return now.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
    
    def estimate_duration(self, task_description, category):
        """
        Estimate task duration based on type and category
        
        Args:
            task_description (str): Task description
            category (str): Task category
            
        Returns:
            int: Duration in minutes
        """
        description_lower = task_description.lower()
        
        # Category-based defaults
        category_durations = {
            'calls': 30,
            'emails': 15,
            'shopping': 60,
            'health': 60,
            'finance': 30,
            'home': 90,
            'social': 120,
            'learning': 60,
            'travel': 180,
            'work': 60
        }
        
        # Quick tasks (override category)
        if any(word in description_lower for word in ['quick', 'briefly', 'check']):
            return 15
        
        # Specific keywords
        if 'meeting' in description_lower:
            return 60
        if 'appointment' in description_lower or 'doctor' in description_lower:
            return 60
        if 'gym' in description_lower or 'workout' in description_lower:
            return 60
        if 'call' in description_lower or 'phone' in description_lower:
            return 30
        if 'email' in description_lower:
            return 15
        
        # Use category default or fallback to 30
        return category_durations.get(category, 30)
    
    def create_event(self, task, calendar_id='primary'):
        """
        Create a Google Calendar event from a task
        
        Args:
            task (dict): Task with title, category, dueDate, priority
            calendar_id (str): Google Calendar ID (default: primary)
            
        Returns:
            dict: Created event or None if failed
        """
        try:
            # Parse date
            start_time = self.parse_natural_date(task.get('dueDate'))
            
            # Estimate duration
            duration = self.estimate_duration(
                task.get('title', ''),
                task.get('category', '')
            )
            end_time = start_time + timedelta(minutes=duration)
            
            # Create event
            event = {
                'summary': task.get('title', 'Untitled Task'),
                'description': task.get('notes', ''),
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'America/Los_Angeles',  # Change to your timezone
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'America/Los_Angeles',
                },
                'colorId': self._get_color_for_priority(task.get('priority', 'medium'))
            }
            
            # Create the event
            created_event = self.service.events().insert(
                calendarId=calendar_id,
                body=event
            ).execute()
            
            print(f"   📅 Created: {task.get('title')} on {start_time.strftime('%A, %B %d at %I:%M %p')}")
            return created_event
            
        except HttpError as error:
            print(f"   ❌ Error creating event: {error}")
            return None
    
    def _get_color_for_priority(self, priority):
        """Map priority to Google Calendar color"""
        colors = {
            'urgent': '11',    # Red
            'high': '11',      # Red
            'medium': '5',     # Yellow
            'low': '10'        # Green/Blue
        }
        return colors.get(priority.lower(), '5')
    
    def create_events_from_json(self, json_data):
        """
        Create multiple events from formatted JSON
        
        Args:
            json_data (str or dict): JSON with reminders array
            
        Returns:
            list: Created events
        """
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
        
        created_events = []
        reminders = data.get('reminders', [])
        
        print(f"\n📅 Creating {len(reminders)} calendar event(s)...")
        
        for reminder in reminders:
            event = self.create_event(reminder)
            if event:
                created_events.append(event)
        
        return created_events

if __name__ == "__main__":
    # Test the calendar manager
    manager = CalendarManager()
    
    # Test event
    test_task = {
        "title": "Test: Buy groceries",
        "notes": "Category: shopping\nPriority: medium",
        "dueDate": "tomorrow",
        "priority": "medium",
        "category": "shopping"
    }
    
    manager.create_event(test_task)
    print("\nCheck your Google Calendar!")