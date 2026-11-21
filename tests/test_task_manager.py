"""Basic automated tests for task validation and JSON storage."""
import tempfile
import unittest
from pathlib import Path
from task_manager.models import validate_title, validate_priority, validate_due_date
from task_manager.storage import TaskStorage

class ValidationTests(unittest.TestCase):
    def test_title_is_trimmed(self):
        self.assertEqual(validate_title("  Study Python  "), "Study Python")

    def test_empty_title_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_title("   ")

    def test_priority_is_case_insensitive(self):
        self.assertEqual(validate_priority("HIGH"), "high")

    def test_invalid_date_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_due_date("21-11-2026")

class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = TaskStorage(Path(self.temp_dir.name) / "tasks.json")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_reload_task(self):
        created = self.storage.add("Finish project", priority="high")
        reloaded = self.storage.get_all()
        self.assertEqual(len(reloaded), 1)
        self.assertEqual(reloaded[0].task_id, created.task_id)
        self.assertEqual(reloaded[0].title, "Finish project")

    def test_complete_task(self):
        task = self.storage.add("Test completion")
        updated = self.storage.mark_completed(task.task_id)
        self.assertTrue(updated.completed)

    def test_delete_task(self):
        task = self.storage.add("Temporary task")
        self.assertTrue(self.storage.delete(task.task_id))
        self.assertEqual(self.storage.get_all(), [])

if __name__ == "__main__":
    unittest.main()
