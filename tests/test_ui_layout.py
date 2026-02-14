
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pyfeed
import curses

class MockWindow:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.buffer = [[' ' for _ in range(width)] for _ in range(height)]
        self.attr = 0
    
    def getmaxyx(self):
        return self.height, self.width
    
    def addstr(self, y, x, string, attr=0):
        if y >= self.height or x >= self.width:
            return
        for i, char in enumerate(string):
            if x + i < self.width:
                self.buffer[y][x + i] = char
    
    def clear(self):
        # In our test we might not want to fully clear to detect overlaps if we draw sequentially without clear
        # But draw_left_pane calls clear() in original code, but I removed it in my edit to just clear the area.
        # Actually I added specific clearing loops.
        pass
        
    def refresh(self):
        pass
        
    def attron(self, attr): self.attr = attr
    def attroff(self, attr): self.attr = 0

class TestUILayout(unittest.TestCase):
    def setUp(self):
        self.height = 20
        self.width = 80
        self.stdscr = MockWindow(self.height, self.width)
        self.left_w = self.width // 3 # 26

    def test_left_pane_width_constraint(self):
        # Create a very long feed name
        long_name = "A" * 50
        csv_files = [long_name]
        
        pyfeed.draw_left_pane(self.stdscr, csv_files, 0, self.left_w)
        
        # Check that we drew the separator at left_w - 1 (25)
        self.assertEqual(self.stdscr.buffer[0][self.left_w - 1], '|')
        self.assertEqual(self.stdscr.buffer[1][self.left_w - 1], '|')
        
        # Check that content does not go beyond left_w - 2 (24)
        # Position 24 might be '…' or a char depending on truncation logic.
        # In my code: display_item = display_item[:left_w - 3] + "…"
        # left_w = 26. left_w - 3 = 23. So chars at 0..22. '…' at 23.
        # So 24 should be space (or empty/separator if I drew it there)
        # My clean loop: stdscr.addstr(y, 0, " " * (left_w - 1)) -> clears 0 to 24.
        # Then draws separator at 25.
        # Then draws text.
        
        # Verify text is truncated
        # Row 1 (index 1) has the item.
        row_content = "".join(self.stdscr.buffer[1][:self.left_w])
        # Expected: 23 chars + ellipsis + space + |
        # Actually logic: display_item[:23] + "…" -> length 24.
        # So "A"*23 + "…" -> fills 0 to 23.
        # 24 is space (from clear).
        # 25 is '|'.
        
        self.assertEqual(self.stdscr.buffer[1][self.left_w - 1], '|')
        self.assertEqual(self.stdscr.buffer[1][self.left_w - 2], ' ') # Logic check
        self.assertEqual(self.stdscr.buffer[1][self.left_w - 3], '…') # Logic check

    @patch('pyfeed.display_csv')
    def test_right_pane_start_position(self, mock_display_csv):
        # Setup mock return for display_csv
        # Row format: [Read, Date, Owner, Title, Link]
        mock_display_csv.return_value = [['False', '2023-01-01', 'Admin', 'Test Title', 'http://example.com']]
        
        csv_files = ["feed1"]
        
        # Pre-fill buffer with 'L' to simulate left pane content or potential overlap trash
        for y in range(self.height):
            for x in range(self.width):
                self.stdscr.buffer[y][x] = 'L'
                
        # Draw right pane
        pyfeed.draw_right_pane(self.stdscr, csv_files, 0, 0, self.left_w)
        
        # Right pane should start at left_w + 1 = 27.
        # It should clear everything from 27 onwards.
        # Check that 'L' remains at left_w (26) and below.
        
        # Check column 26 (left_w) - should still be 'L' (touched by neither strictly? 
        # Left pane draws separator at 25. 
        # Right pane starts at 27.
        # Column 26 is the gap. 
        # Wait, my implementation:
        # Left pane: clear " " * (left_w - 1) -> 0..24. Separator at 25.
        # Right pane: right_pane_start_x = left_w + 1 = 27.
        # So column 26 is untouched by both?
        # That effectively leaves a 1 char gap between separator and right pane. That's fine.
        
        self.assertEqual(self.stdscr.buffer[5][self.left_w], 'L') 
        
        # Check that right pane area is cleared/drawn
        # At 27 should be space or content.
        # Row 0: "Details:" at 27+1 = 28.
        self.assertEqual(self.stdscr.buffer[0][self.left_w + 2], 'D')
        
        # Check row 1 (content)
        # Should NOT have 'L'
        self.assertNotEqual(self.stdscr.buffer[1][self.left_w + 2], 'L')

if __name__ == '__main__':
    unittest.main()
