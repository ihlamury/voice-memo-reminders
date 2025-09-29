"""
Reminder Manager - Formats categorized tasks for iOS Shortcuts
"""
import json

class ReminderManager:
    def __init__(self):
        """Initialize reminder manager"""
        pass
    
    def format_reminders(self, categorized_tasks):
        """
        Format categorized tasks into a structure iOS Shortcuts can use
        
        Args:
            categorized_tasks (dict): Tasks categorized by Claude
            
        Returns:
            str: JSON string formatted for iOS Shortcuts
        """
        if not categorized_tasks or 'tasks' not in categorized_tasks:
            return json.dumps({"reminders": []})
        
        reminders = []
        
        for task in categorized_tasks.get('tasks', []):
            reminder = {
                "title": task.get('description', 'Untitled task'),
                "notes": f"Category: {task.get('category', 'general')}\nPriority: {task.get('priority', 'medium')}",
                "dueDate": task.get('due_date'),
                "list": task.get('category', 'general').capitalize()
            }
            reminders.append(reminder)
        
        return json.dumps({"reminders": reminders}, indent=2)
    
    def get_reminder_lists(self, categorized_tasks):
        """
        Get unique list names from categorized tasks
        
        Args:
            categorized_tasks (dict): Tasks categorized by Claude
            
        Returns:
            list: Unique category/list names
        """
        if not categorized_tasks or 'tasks' not in categorized_tasks:
            return []
        
        categories = set()
        for task in categorized_tasks.get('tasks', []):
            category = task.get('category', 'general')
            categories.add(category.capitalize())
        
        return sorted(list(categories))

if __name__ == "__main__":
    # Test the reminder manager
    sample_tasks = {
        "tasks": [
            {
                "description": "Buy milk and eggs",
                "priority": "medium",
                "category": "shopping",
                "due_date": "tomorrow"
            },
            {
                "description": "Call dentist",
                "priority": "high",
                "category": "health",
                "due_date": "Monday"
            }
        ]
    }
    
    manager = ReminderManager()
    formatted = manager.format_reminders(sample_tasks)
    print(formatted)
