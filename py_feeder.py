import curses
import feedparser

def fetch_rss_feed(url):
    """Fetches the RSS feed and returns a list of entries."""
    feed = feedparser.parse(url)
    return feed.feed.title, [{'title': entry.title, 'summary': entry.summary} for entry in feed.entries]

def truncate_text(text, max_width):
    """Truncates the text to fit within the screen width."""
    if len(text) > max_width:
        return text[:max_width - 3] + "..."  # Add ellipsis to indicate truncation
    return text

def draw_left_pane(stdscr, feed_name):
    """Draws the left pane showing the feed name."""
    stdscr.addstr(0, 0, "Feed: " + feed_name, curses.A_BOLD)

def draw_right_pane(stdscr, rss_feed, selected_idx, pane_width):
    """Draws the right pane showing the details of the selected RSS feed items."""
    height, width = stdscr.getmaxyx()

    # Display the items (titles of the RSS feed)
    start_display_index = 1  # Start after the feed name
    max_items_to_display = height - 3  # Leave space for summary and status bar

    for idx, item in enumerate(rss_feed):
        # Ensure we don't exceed the displayable items
        if idx >= start_display_index + max_items_to_display:
            break

        title = truncate_text(item['title'], pane_width)
        if idx == selected_idx:
            stdscr.addstr(start_display_index + idx - 1, 0, title, curses.A_REVERSE)  # Highlight selected item
        else:
            stdscr.addstr(start_display_index + idx - 1, 0, title)

    # Show details of the selected item (summary)
    if rss_feed:
        summary = truncate_text(rss_feed[selected_idx]['summary'], pane_width)
        stdscr.addstr(height - 2, 0, f"Summary: {summary}")

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()

    # URL of the RSS feed
    rss_url = 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml'
    feed_name, rss_feed = fetch_rss_feed(rss_url)

    if not rss_feed:
        stdscr.addstr(0, 0, "No entries found in RSS feed.")
        stdscr.refresh()
        stdscr.getch()
        return

    selected_idx = 0

    while True:
        height, width = stdscr.getmaxyx()
        right_pane_width = width - 2  # Right pane takes all available width

        stdscr.clear()

        # Draw the left pane with the feed name
        draw_left_pane(stdscr, feed_name)

        # Draw the right pane with the list of items (titles)
        draw_right_pane(stdscr, rss_feed, selected_idx, right_pane_width)

        # Status bar at the bottom
        status_bar = f"Item {selected_idx + 1}/{len(rss_feed)} | Press 'q' to quit"
        stdscr.addstr(height - 2, 0, truncate_text(status_bar, width), curses.A_STANDOUT)

        # Handle user input for navigation
        key = stdscr.getch()

        if key == curses.KEY_UP:
            if selected_idx > 0:
                selected_idx -= 1
        elif key == curses.KEY_DOWN:
            if selected_idx < len(rss_feed) - 1:
                selected_idx += 1
        elif key == ord('q'):  # Press 'q' to quit
            break

        stdscr.refresh()

curses.wrapper(main)
