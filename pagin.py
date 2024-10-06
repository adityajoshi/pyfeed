import curses

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()

    # Sample large list of items (mock RSS feed titles)
    items = [f"Feed {i + 1}: Example title" for i in range(100)]  # 100 mock feeds
    selected_idx = 0
    start_idx = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Number of items that can fit in the screen (minus 2 for status and details)
        visible_items_count = height - 2

        # Calculate the range of items to display (pagination)
        end_idx = start_idx + visible_items_count
        visible_items = items[start_idx:end_idx]

        # Display the visible items
        for idx, item in enumerate(visible_items):
            display_idx = start_idx + idx
            if display_idx == selected_idx:
                stdscr.addstr(idx, 0, item, curses.A_REVERSE)  # Highlight selected item
            else:
                stdscr.addstr(idx, 0, item)

        # Status bar at the bottom
        status_bar = f"Item {selected_idx + 1}/{len(items)} | Press 'q' to quit"
        stdscr.addstr(height - 1, 0, status_bar, curses.A_STANDOUT)

        # Handle user input for navigation
        key = stdscr.getch()

        if key == curses.KEY_UP:
            if selected_idx > 0:
                selected_idx -= 1
                # Scroll up if necessary
                if selected_idx < start_idx:
                    start_idx -= 1
        elif key == curses.KEY_DOWN:
            if selected_idx < len(items) - 1:
                selected_idx += 1
                # Scroll down if necessary
                if selected_idx >= end_idx:
                    start_idx += 1
        elif key == ord('q'):  # Press 'q' to quit
            break

        stdscr.refresh()

curses.wrapper(main)
