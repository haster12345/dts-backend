import unittest
import sqlite3
import os
from datetime import datetime
from src.db import DB  # Import the DB class from your module


class TestDB(unittest.TestCase):
    """Test cases for the DB class."""

    def setUp(self):
        """Set up test environment before each test."""
        # Use a test database file
        self.db = DB()
        self.db.db = "test_tasks.db"
        self.db._create_tables()

        # Sample task data for testing
        self.sample_task = {
            'id': None,  # SQLite will auto-assign this for new records
            'CaseNumber': 12345,
            'title': 'Test Task',
            'description': 'This is a test task description',
            'status': 'Open',
            'CreatedDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def tearDown(self):
        """Clean up after each test."""
        # Delete the test database file
        if os.path.exists(self.db.db):
            os.remove(self.db.db)

    def test_create_tables(self):
        """Test if tables are created properly."""
        con = sqlite3.connect(self.db.db)
        cursor = con.cursor()

        # Check if the tasks table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
        table_exists = cursor.fetchone()
        con.close()

        self.assertIsNotNone(table_exists)

    def test_create_and_get_tasks(self):
        """Test creating a task and retrieving it."""
        # Create a task
        self.db.create_tasks(self.sample_task)

        # Retrieve all tasks
        tasks = self.db.get_tasks()

        # Check if we have exactly one task
        self.assertEqual(len(tasks), 1)

        # Check if the task details match
        task = tasks[0]
        self.assertEqual(task['CaseNumber'], self.sample_task['CaseNumber'])
        self.assertEqual(task['title'], self.sample_task['title'])
        self.assertEqual(task['description'], self.sample_task['description'])
        self.assertEqual(task['status'], self.sample_task['status'])
        self.assertEqual(task['CreatedDate'], self.sample_task['CreatedDate'])

    def test_update_task_case_number(self):
        """Test updating a task's case number."""
        # Create a task
        self.db.create_tasks(self.sample_task)

        # Get the task to find its ID
        tasks = self.db.get_tasks()
        task_id = tasks[0]['id']

        # Update the case number
        new_case_number = 67890
        self.db.update_task_case_number(task_id, new_case_number)

        # Get the updated task
        updated_tasks = self.db.get_tasks()
        updated_task = updated_tasks[0]

        # Check if the case number was updated
        self.assertEqual(updated_task['CaseNumber'], new_case_number)

    def test_update_task_description(self):
        """Test updating a task's description."""
        # Create a task
        self.db.create_tasks(self.sample_task)

        # Get the task to find its ID
        tasks = self.db.get_tasks()
        task_id = tasks[0]['id']

        # Update the description
        new_description = "Updated description for testing"
        self.db.update_task_description(task_id, new_description)

        # Get the updated task
        updated_tasks = self.db.get_tasks()
        updated_task = updated_tasks[0]

        # Check if the description was updated
        self.assertEqual(updated_task['description'], new_description)

    def test_delete_task(self):
        """Test deleting a task."""
        # Create a task
        self.db.create_tasks(self.sample_task)

        # Get the task to find its ID
        tasks = self.db.get_tasks()
        task_id = tasks[0]['id']

        # Delete the task
        self.db.delete_task({'id': task_id})

        # Check if the task was deleted
        tasks_after_delete = self.db.get_tasks()
        self.assertEqual(len(tasks_after_delete), 0)

    def test_multiple_tasks(self):
        """Test handling multiple tasks."""
        # Create multiple tasks
        task1 = self.sample_task.copy()
        task2 = self.sample_task.copy()
        task2['CaseNumber'] = 54321
        task2['title'] = 'Second Test Task'

        self.db.create_tasks(task1)
        self.db.create_tasks(task2)

        # Check if both tasks were created
        tasks = self.db.get_tasks()
        self.assertEqual(len(tasks), 2)

        # Verify the tasks have different case numbers
        case_numbers = [task['CaseNumber'] for task in tasks]
        self.assertIn(12345, case_numbers)
        self.assertIn(54321, case_numbers)


if __name__ == '__main__':
    unittest.main()