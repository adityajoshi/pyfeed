import curses

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()

    # Sample list of items (mock RSS feed titles)
    items = ["Feed 1: Latest News", "Feed 2: Tech Updates", "Feed 3: Sports Highlights",
             "Feed 4: Weather Forecast", "Feed 5: Market Trends", "Feed 6: Entertainment"]

    # Set initial index for selected item
    selected_idx = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Display the list of items
        for idx, item in enumerate(items):
            if idx == selected_idx:
                stdscr.addstr(idx, 0, item, curses.A_REVERSE)  # Highlight the selected item
            else:
                stdscr.addstr(idx, 0, item)

        # Handle user input for navigation
        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected_idx = max(0, selected_idx - 1)
        elif key == curses.KEY_DOWN:
            selected_idx = min(len(items) - 1, selected_idx + 1)
        elif key == ord('q'):  # Press 'q' to quit
            break

        stdscr.refresh()

curses.wrapper(main)
