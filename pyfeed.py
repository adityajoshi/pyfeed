import curses
import csv
import os
import webbrowser
import common

#csv_files = ["Feed 1", "Feed 2", "Feed 3", "Feed 4", "Feed 5"]
#csv_files = []
# Sample data for the left pane

# Function to find all CSV files in the folder
def find_csv_files():
    feeds_path = common.FEEDS_DIR
    if not os.path.exists(feeds_path):
        return []
    return [f for f in os.listdir(feeds_path)]

def display_csv(file_name):
    try:
        feed_path = os.path.join(common.FEEDS_DIR, file_name)
        if not os.path.exists(feed_path):
            raise FileNotFoundError(f"The feed file {feed_path} does not exist.")
        with open(feed_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            if rows:
                return rows
            else:
                return []
    except Exception as e:
        return str(e)


# Function to update the CSV file to mark items as read
def update_csv(file_name, link, status):
    feed_path = os.path.join(common.FEEDS_DIR, file_name)
    rows = []

    # Read the CSV and update the status of the matching link
    with open(feed_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        for row in rows:
            if row[4] == link:  # Match based on link
                row[0] = status  # Update the "Read" status


    # Write the updated rows back to the CSV file
    with open(feed_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

def update_all(file_name, status):
    feed_path = os.path.join(common.FEEDS_DIR, file_name)
    rows = []

    # Read the CSV and update the status of the matching title
    with open(feed_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        for row in rows:
            row[0] = status  # Update the "Read" status


    # Write the updated rows back to the CSV file
    with open(feed_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)


# Function to open a URL in the default browser
def open_link(link):
    webbrowser.open_new(link)


def draw_left_pane(stdscr, csv_files, selected_idx, left_w):
    """Draws the left pane showing the list of items."""
    # Clear left pane area
    height, width = stdscr.getmaxyx()
    for y in range(height):
        stdscr.addstr(y, 0, " " * (left_w - 1))
        stdscr.addstr(y, left_w - 1, "|") # Vertical separator

    stdscr.addstr(0, 0, "Feeds:", curses.A_BOLD)

    max_rows_to_display = height - 2  # Leave room for title and status bar
    start_row = max(0, selected_idx - max_rows_to_display + 1)
    end_row = min(start_row + max_rows_to_display, len(csv_files))
    
    for idx, item in enumerate(csv_files[start_row:end_row]):
        # Truncate item name if it's too long
        display_item = item
        if len(display_item) > left_w - 2:
             display_item = display_item[:left_w - 3] + "…"
        
        if start_row + idx == selected_idx:
            stdscr.addstr(idx + 1, 0, display_item, curses.A_REVERSE)  # Highlight selected item
        else:
            stdscr.addstr(idx + 1, 0, display_item)

def draw_right_pane(stdscr, csv_files, selected_idx, selected_item_idx, left_w):
    """Draws the right pane showing the details of the selected item."""
    height, width = stdscr.getmaxyx()
    right_pane_start_x = left_w + 1
    right_pane_width = width - right_pane_start_x
    
    # Clear right pane area
    for y in range(height - 1): # Leave status bar line
        stdscr.addstr(y, right_pane_start_x, " " * (right_pane_width - 1))

    rows = 0
    csv_data = [] # Initialize csv_data to safe default
    if csv_files:
        feed_name = csv_files[selected_idx]
        #details = data[feed_name]
        csv_data = display_csv(feed_name)
        if isinstance(csv_data, str):  # In case of an error
            stdscr.addstr(0, right_pane_start_x + 1, f"Error loading {feed_name}: {csv_data}")
        else:
            rows = len(csv_data)
            stdscr.addstr(0, right_pane_start_x + 1, "Details:", curses.A_BOLD)
            # Limit the display to the terminal's height minus space for title/status
            max_rows_to_display = height - 2  # Leave room for title and status bar
            start_row = max(0, selected_item_idx - max_rows_to_display + 1)
            end_row = min(start_row + max_rows_to_display, rows)

            for idx, each_row in enumerate(csv_data[start_row:end_row]):
                display_row = "  ".join(each_row[1::2])  # Display only first 4 columns (Read, Date, Owner, Title)
                
                # Truncate to fit right pane
                if len(display_row) > right_pane_width - 2:
                    display_row = display_row[:right_pane_width - 3] + "…"

                if start_row + idx == selected_item_idx:
                    if each_row[0].lower() != 'true':
                        stdscr.attron(curses.A_BOLD)
                        stdscr.addstr(idx+1, right_pane_start_x + 1, display_row, curses.A_REVERSE)
                        stdscr.attroff(curses.A_BOLD)
                    else:
                        stdscr.addstr(idx+1, right_pane_start_x + 1, display_row, curses.A_REVERSE)
                else:
                    if each_row[0].lower() != 'true':
                        stdscr.attron(curses.A_BOLD)
                        stdscr.addstr(idx+1, right_pane_start_x + 1, display_row)
                        stdscr.attroff(curses.A_BOLD)
                    else:
                        stdscr.addstr(idx+1, right_pane_start_x + 1, display_row)
    return csv_data

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    selected_idx = 0
    selected_item_idx = 0
    SELECTED_PANE = 0
    csv_files = find_csv_files()
    # 0 is for left, 1 for right

    while True:
        height, width = stdscr.getmaxyx()

        left_w = width // 3

        # Draw the left pane
        draw_left_pane(stdscr, csv_files, selected_idx, left_w)

        # Draw the right pane
        csv_data = draw_right_pane(stdscr, csv_files, selected_idx, selected_item_idx, left_w)

        # Status bar at the bottom
        stdscr.addstr(height - 1, 0, "Press 'q' to quit, Arrow keys to navigate.", curses.A_DIM)

        stdscr.refresh()

        # Handle user input for navigation
        key = stdscr.getch()

        if key == curses.KEY_UP or key == ord('k'):
            if selected_idx > 0 and SELECTED_PANE == 0:
                selected_idx -= 1
                selected_item_idx = 0
            if selected_item_idx > 0 and SELECTED_PANE == 1:
                selected_item_idx -= 1
        elif key == curses.KEY_DOWN or key == ord('j'):
            if selected_idx < len(csv_files) - 1 and SELECTED_PANE == 0:
                selected_idx += 1
                selected_item_idx = 0
            if selected_item_idx < len(csv_data) - 1 and SELECTED_PANE == 1:
                selected_item_idx += 1
        elif key == ord('g'):
            if SELECTED_PANE == 0:
                selected_idx = 0
            if SELECTED_PANE == 1:
                selected_item_idx = 0
        elif key == ord('G'):
            if SELECTED_PANE == 0:
                selected_idx = len(csv_files) - 1
            if SELECTED_PANE == 1:
                selected_item_idx = len(csv_data) - 1
        elif key == curses.KEY_LEFT or key == ord('h'):
            if SELECTED_PANE == 1:
                SELECTED_PANE = 0
        elif key == curses.KEY_RIGHT or key == ord('l'):
            if SELECTED_PANE == 0:
                SELECTED_PANE = 1
        elif key == ord('\n'):  # Press 'enter' to open in browser
            if csv_data:
                link = csv_data[selected_item_idx][4] # Get link from selected row
                open_link(link)
        elif key == ord('r') and csv_data:
            # Mark the selected row as read
            csv_data[selected_item_idx][0] = 'True'  # +1 due to header row
            update_csv(csv_files[selected_idx], csv_data[selected_item_idx][4], 'True')
        elif key == ord('F') and csv_data:
            # Mark the selected file as read
            update_all(csv_files[selected_idx], 'True')
        elif key == ord('q'):  # Press 'q' to quit
            break

if __name__ == "__main__":
    curses.wrapper(main)
