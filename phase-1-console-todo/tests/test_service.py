"""Unit tests for TodoService"""

import unittest
from datetime import datetime, timedelta
from src.domain.models import Task, TaskStatus, Priority, Recurrence
from src.domain.exceptions import ValidationError, TaskNotFoundError
from src.repository.memory import InMemoryTodoRepository
from src.service.todo_service import TodoService


class TestTodoService(unittest.TestCase):
    """Test TodoService business logic"""
    
    def setUp(self):
        """Set up test service"""
        repo = InMemoryTodoRepository()
        self.service = TodoService(repo)
    
    def test_add_task_minimal(self):
        """Test adding task with minimal fields"""
        task = self.service.add_task(title="Test Task")
        
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertEqual(task.priority, Priority.MEDIUM)
    
    def test_add_task_with_all_fields(self):
        """Test adding task with all fields"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        task = self.service.add_task(
            title="Complete Task",
            description="Test description",
            priority=Priority.HIGH,
            tags=["work", "urgent"],
            due_date=tomorrow,
            recurrence=Recurrence.DAILY,
        )
        
        self.assertEqual(task.title, "Complete Task")
        self.assertEqual(task.description, "Test description")
        self.assertEqual(task.priority, Priority.HIGH)
        self.assertEqual(task.tags, ["work", "urgent"])
        self.assertIsNotNone(task.due_date)
        self.assertEqual(task.recurrence, Recurrence.DAILY)
    
    def test_add_task_past_due_date_raises_error(self):
        """Test adding task with past due date raises error"""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        with self.assertRaises(ValidationError):
            self.service.add_task(title="Test", due_date=yesterday)
    
    def test_add_task_invalid_date_format_raises_error(self):
        """Test adding task with invalid date format raises error"""
        with self.assertRaises(ValidationError):
            self.service.add_task(title="Test", due_date="2025-13-45")
    
    def test_get_all_tasks(self):
        """Test retrieving all tasks"""
        self.service.add_task(title="Task 1")
        self.service.add_task(title="Task 2")
        
        tasks = self.service.get_all_tasks()
        self.assertEqual(len(tasks), 2)
    
    def test_get_task_by_id(self):
        """Test retrieving task by ID"""
        task = self.service.add_task(title="Test Task")
        retrieved = self.service.get_task_by_id(task.id)
        
        self.assertEqual(retrieved.id, task.id)
    
    def test_get_task_by_id_not_found_raises_error(self):
        """Test retrieving non-existent task raises error"""
        with self.assertRaises(TaskNotFoundError):
            self.service.get_task_by_id("non-existent-id")
    
    def test_update_task(self):
        """Test updating task fields"""
        task = self.service.add_task(title="Original")
        updated = self.service.update_task(
            task.id,
            title="Updated",
            priority=Priority.URGENT
        )
        
        self.assertEqual(updated.title, "Updated")
        self.assertEqual(updated.priority, Priority.URGENT)
    
    def test_delete_task(self):
        """Test deleting a task"""
        task = self.service.add_task(title="Test Task")
        result = self.service.delete_task(task.id)
        
        self.assertTrue(result)
        with self.assertRaises(TaskNotFoundError):
            self.service.get_task_by_id(task.id)
    
    def test_toggle_complete(self):
        """Test toggling task completion"""
        task = self.service.add_task(title="Test Task")
        
        # Mark complete
        updated = self.service.toggle_complete(task.id)
        self.assertEqual(updated.status, TaskStatus.COMPLETED)
        self.assertIsNotNone(updated.completed_at)
        
        # Mark pending
        updated = self.service.toggle_complete(task.id)
        self.assertEqual(updated.status, TaskStatus.PENDING)
        self.assertIsNone(updated.completed_at)
    
    def test_toggle_complete_recurring_creates_next(self):
        """Test completing recurring task creates next instance"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        task = self.service.add_task(
            title="Daily Task",
            due_date=tomorrow,
            recurrence=Recurrence.DAILY
        )
        
        # Complete the task
        self.service.toggle_complete(task.id)
        
        # Should have 2 tasks now (original completed + new instance)
        all_tasks = self.service.get_all_tasks()
        self.assertEqual(len(all_tasks), 2)
        
        # Find the new pending task
        pending_tasks = [t for t in all_tasks if t.status == TaskStatus.PENDING]
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(pending_tasks[0].title, "Daily Task")
    
    def test_search_by_title(self):
        """Test searching tasks by title"""
        self.service.add_task(title="Buy groceries")
        self.service.add_task(title="Read book")
        self.service.add_task(title="Buy tickets")
        
        results = self.service.search_tasks(query="buy")
        self.assertEqual(len(results), 2)
    
    def test_search_by_tag(self):
        """Test filtering tasks by tag"""
        self.service.add_task(title="Task 1", tags=["work"])
        self.service.add_task(title="Task 2", tags=["personal"])
        self.service.add_task(title="Task 3", tags=["work", "urgent"])
        
        results = self.service.search_tasks(tag="work")
        self.assertEqual(len(results), 2)
    
    def test_search_by_status(self):
        """Test filtering tasks by status"""
        task1 = self.service.add_task(title="Task 1")
        task2 = self.service.add_task(title="Task 2")
        self.service.toggle_complete(task1.id)
        
        pending = self.service.search_tasks(status=TaskStatus.PENDING)
        completed = self.service.search_tasks(status=TaskStatus.COMPLETED)
        
        self.assertEqual(len(pending), 1)
        self.assertEqual(len(completed), 1)
    
    def test_search_by_priority(self):
        """Test filtering tasks by priority"""
        self.service.add_task(title="Task 1", priority=Priority.LOW)
        self.service.add_task(title="Task 2", priority=Priority.URGENT)
        self.service.add_task(title="Task 3", priority=Priority.URGENT)
        
        results = self.service.search_tasks(priority=Priority.URGENT)
        self.assertEqual(len(results), 2)
    
    def test_search_multiple_filters(self):
        """Test searching with multiple filters (AND logic)"""
        self.service.add_task(
            title="Work meeting",
            tags=["work"],
            priority=Priority.HIGH
        )
        self.service.add_task(
            title="Work email",
            tags=["work"],
            priority=Priority.LOW
        )
        
        results = self.service.search_tasks(
            tag="work",
            priority=Priority.HIGH
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Work meeting")
    
    def test_sort_by_priority(self):
        """Test sorting tasks by priority"""
        self.service.add_task(title="Low", priority=Priority.LOW)
        self.service.add_task(title="Urgent", priority=Priority.URGENT)
        self.service.add_task(title="Medium", priority=Priority.MEDIUM)
        
        tasks = self.service.get_all_tasks()
        sorted_tasks = self.service.sort_tasks(tasks, "priority")
        
        self.assertEqual(sorted_tasks[0].priority, Priority.URGENT)
        self.assertEqual(sorted_tasks[-1].priority, Priority.LOW)
    
    def test_sort_by_due_date(self):
        """Test sorting tasks by due date"""
        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        self.service.add_task(title="Tomorrow", due_date=tomorrow)
        self.service.add_task(title="Today", due_date=today)
        self.service.add_task(title="No date")
        
        tasks = self.service.get_all_tasks()
        sorted_tasks = self.service.sort_tasks(tasks, "due_date")
        
        self.assertEqual(sorted_tasks[0].title, "Today")
        self.assertEqual(sorted_tasks[-1].title, "No date")
    
    def test_sort_by_created(self):
        """Test sorting tasks by creation date"""
        task1 = self.service.add_task(title="First")
        task2 = self.service.add_task(title="Second")
        
        tasks = self.service.get_all_tasks()
        sorted_tasks = self.service.sort_tasks(tasks, "created")
        
        # Newest first
        self.assertEqual(sorted_tasks[0].id, task2.id)
    
    def test_sort_by_status(self):
        """Test sorting tasks by status"""
        task1 = self.service.add_task(title="Task 1")
        task2 = self.service.add_task(title="Task 2")
        self.service.toggle_complete(task1.id)
        
        tasks = self.service.get_all_tasks()
        sorted_tasks = self.service.sort_tasks(tasks, "status")
        
        # PENDING first
        self.assertEqual(sorted_tasks[0].status, TaskStatus.PENDING)
    
    def test_sort_invalid_criteria_raises_error(self):
        """Test sorting with invalid criteria raises error"""
        tasks = self.service.get_all_tasks()
        
        with self.assertRaises(ValidationError):
            self.service.sort_tasks(tasks, "invalid")


if __name__ == "__main__":
    unittest.main()
