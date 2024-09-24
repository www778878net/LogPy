import unittest
from src.log_entry import LogEntry, BasicInfo

class TestLogEntry(unittest.TestCase):
    def test_log_entry_creation(self):
        entry = LogEntry()
        entry.basic.message = "Test message"
        entry.basic.summary = "Test summary"
        self.assertEqual(entry.basic.message, "Test message")
        self.assertEqual(entry.basic.summary, "Test summary")

    def test_log_entry_to_json(self):
        entry = LogEntry()
        entry.basic.message = "Test message"
        entry.basic.summary = "Test summary"
        json_data = entry.to_json()
        self.assertIn("message", json_data)
        self.assertIn("summary", json_data)

if __name__ == '__main__':
    unittest.main()