import curses
import csv
import os
import webbrowser

FEED_FOLDER = 'feeds'

#csv_files = ["Feed 1", "Feed 2", "Feed 3", "Feed 4", "Feed 5"]
#csv_files = []
# Sample data for the left pane

# Function to find all CSV files in the folder
def find_csv_files():
    folder_path = os.path.join(os.getcwd(), FEED_FOLDER)
    if not os.path.exists(folder_path):
        return []
    return [f for f in os.listdir(folder_path) if f.endswith('.csv')]

def display_csv(file_name):
    try:
        with open(os.path.join(FEED_FOLDER, file_name), newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            if rows:
                return rows
            else:
                return []
    except Exception as e:
        return str(e)


# Function to open a URL in the default browser
def open_link(link):
    webbrowser.open_new(link)


def draw_left_pane(stdscr, csv_files, selected_idx, left_w):
    """Draws the left pane showing the list of items."""
    stdscr.clear()
    stdscr.addstr(0, 0, "Feeds:", curses.A_BOLD)
    
    for idx, item in enumerate(csv_files):
        if idx == selected_idx:
            stdscr.addstr(idx + 1, 0, item, curses.A_REVERSE)  # Highlight selected item
        else:
            stdscr.addstr(idx + 1, 0, item)

def draw_right_pane(stdscr, csv_files, selected_idx, selected_item_idx, left_w):
    """Draws the right pane showing the details of the selected item."""
    #import ipdb; ipdb.set_trace()
    height, width = stdscr.getmaxyx()
    rows = 0
    if csv_files:
        feed_name = csv_files[selected_idx]
        #details = data[feed_name]
        csv_data = display_csv(feed_name)
        if isinstance(csv_data, str):  # In case of an error
            stdscr.addstr(0, left_w // 2+2, f"Error loading {feed_name}: {csv_data}")
        else:
            rows = len(csv_data)
            stdscr.addstr(0, left_w // 2 + 2, "Details:", curses.A_BOLD)
            # Limit the display to the terminal's height minus space for title/status
            max_rows_to_display = height - 2  # Leave room for title and status bar
            start_row = max(0, selected_item_idx - max_rows_to_display + 1)
            end_row = min(start_row + max_rows_to_display, rows)

            for idx, each_row in enumerate(csv_data[start_row:end_row]):
                display_row = "  ".join(each_row[1::2])  # Display only first 4 columns (Read, Date, Owner, Title)
                if start_row + idx == selected_item_idx:
                    stdscr.addstr(idx+1, left_w // 2 + 2, display_row, curses.A_REVERSE)
                else:
                    stdscr.addstr(idx+1, left_w // 2 + 2, display_row)
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
            if selected_item_idx > 0 and SELECTED_PANE == 1:
                selected_item_idx -= 1
        elif key == curses.KEY_DOWN or key == ord('j'):
            if selected_idx < len(csv_files) - 1 and SELECTED_PANE == 0:
                selected_idx += 1
            if selected_item_idx < len(csv_data) - 1 and SELECTED_PANE == 1:
                selected_item_idx += 1
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
        elif key == ord('q'):  # Press 'q' to quit
            break

curses.wrapper(main)
