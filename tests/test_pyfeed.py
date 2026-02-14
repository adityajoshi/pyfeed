import unittest
import os
import shutil
import csv
import tempfile
from unittest.mock import patch, MagicMock
import common
import pyfeed_update
import pyfeed

class TestPyfeed(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_feeds_dir = common.FEEDS_DIR
        common.FEEDS_DIR = self.test_dir

        self.csv_file = "test_feed_records"
        self.csv_path = os.path.join(self.test_dir, self.csv_file)

        # Create a sample CSV file
        # Format: Read, Date, Author, Title, Link
        self.initial_data = [
            ["False", "20231026000000", "Author1", "Same Title", "http://example.com/1"],
            ["False", "20231025000000", "Author2", "Other Title", "http://example.com/2"]
        ]

        with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(self.initial_data)

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        common.FEEDS_DIR = self.original_feeds_dir

    def test_load_existing_records(self):
        """Test that load_existing_records reads links (column 4)."""
        links = pyfeed_update.load_existing_records(self.csv_file)
        self.assertIn("http://example.com/1", links)
        self.assertIn("http://example.com/2", links)
        self.assertEqual(len(links), 2)

    def test_unique_filtering_logic(self):
        """Test that new entries with different links but same title are preserved."""
        # This duplicates the logic in pyfeed_update.update()

        existing_records = pyfeed_update.load_existing_records(self.csv_file)

        new_entries = [
            ("False", "20231027000000", "Author1", "Same Title", "http://example.com/3"), # Same title, new link
            ("False", "20231026000000", "Author1", "Same Title", "http://example.com/1"), # Duplicate link
        ]

        # The fix: filter based on entry[4] (Link)
        unique_entries = [entry for entry in new_entries if entry[4] not in existing_records]

        self.assertEqual(len(unique_entries), 1)
        self.assertEqual(unique_entries[0][4], "http://example.com/3")

    def test_update_csv_status(self):
        """Test that update_csv updates status based on Link."""
        # Mark the item with "Same Title" (link http://example.com/1) as read
        pyfeed.update_csv(self.csv_file, "http://example.com/1", "True")

        with open(self.csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Row 0 should be True
        self.assertEqual(rows[0][0], "True")
        self.assertEqual(rows[0][4], "http://example.com/1")

        # Row 1 should remain False
        self.assertEqual(rows[1][0], "False")
        self.assertEqual(rows[1][4], "http://example.com/2")

    def test_format_display_date(self):
        """Test the date formatting function."""
        # Test valid date format
        date_str = "20241119222120"
        expected = "19-NOV-2024"
        self.assertEqual(pyfeed.format_display_date(date_str), expected)

        # Test another valid date
        date_str = "20230101000000"
        expected = "01-JAN-2023"
        self.assertEqual(pyfeed.format_display_date(date_str), expected)

        # Test invalid date format (should return original string)
        invalid_date = "invalid-date"
        self.assertEqual(pyfeed.format_display_date(invalid_date), invalid_date)

    def test_find_index_string(self):
        data = ["Apple", "Banana", "Cherry"]
        self.assertEqual(pyfeed.find_index(data, "ban"), 1)
        self.assertEqual(pyfeed.find_index(data, "cherry"), 2)
        self.assertEqual(pyfeed.find_index(data, "xyz"), -1)
        self.assertEqual(pyfeed.find_index(data, "Apple"), 0)

    def test_find_index_with_key_func(self):
        data = [
            {"name": "Item 1", "desc": "Desc 1"},
            {"name": "Item 2", "desc": "Desc 2"},
        ]
        key_func = lambda x: x["name"]
        self.assertEqual(pyfeed.find_index(data, "item 2", key_func), 1)
        self.assertEqual(pyfeed.find_index(data, "item 1", key_func), 0)
        self.assertEqual(pyfeed.find_index(data, "xyz", key_func), -1)

    def test_find_next(self):
        data = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Banana"]
        # Find next "Banana" starting from index 1 (should find index 5)
        self.assertEqual(pyfeed.find_next(data, "Banana", 1), 5)
        # Find next "Banana" starting from index 5 (wrap around to 1)
        self.assertEqual(pyfeed.find_next(data, "Banana", 5), 1)
        # Find next "Apple" starting from index 2 (wrap around to 0)
        self.assertEqual(pyfeed.find_next(data, "Apple", 2), 0)
        # No match
        self.assertEqual(pyfeed.find_next(data, "Fig", 0), -1)

    def test_find_prev(self):
        data = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Banana"]
        # Find prev "Banana" starting from index 5 (should find index 1)
        self.assertEqual(pyfeed.find_prev(data, "Banana", 5), 1)
        # Find prev "Banana" starting from index 1 (wrap around to 5)
        self.assertEqual(pyfeed.find_prev(data, "Banana", 1), 5)
        # Find prev "Apple" starting from index 2 (should find index 0)
        self.assertEqual(pyfeed.find_prev(data, "Apple", 2), 0)
        # No match
        self.assertEqual(pyfeed.find_prev(data, "Fig", 0), -1)

if __name__ == '__main__':
    unittest.main()
