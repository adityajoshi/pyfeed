import curses

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()

    # Sample list of items (mock RSS feed titles)
    items = [
        "Feed 1: Latest News",
        "Feed 2: Tech Updates",
        "Feed 3: Sports Highlights",
        "Feed 4: Weather Forecast",
        "Feed 5: Market Trends",
        "Feed 6: Entertainment"
    ]

    # Mock details corresponding to each feed item
    details = [
        "Latest headlines from around the world.",
        "Updates on the latest tech products and innovations.",
        "Highlights and scores from recent sporting events.",
        "Current weather conditions and forecasts.",
        "Trends and updates from financial markets.",
        "The latest in movies, shows, and celebrity news."
    ]

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

        # Status bar at the bottom
        status_bar = f"Item {selected_idx + 1}/{len(items)} | Press 'q' to quit"
        stdscr.addstr(height - 1, 0, status_bar, curses.A_STANDOUT)

        # Show details of the selected item at the bottom
        stdscr.addstr(height - 2, 0, f"Details: {details[selected_idx]}")

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
