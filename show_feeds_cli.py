import os
import csv
import curses
import webbrowser

FEED_FOLDER = 'feeds'


# Function to find all CSV files in the folder
def find_csv_files():
    folder_path = os.path.join(os.getcwd(), FEED_FOLDER)
    if not os.path.exists(folder_path):
        return []
    return [f for f in os.listdir(folder_path) if f.endswith('.csv')]


# Function to read the selected CSV file and return its content
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


# Function to update the CSV file to mark items as read
def update_csv(file_name, title, status):
    file_path = os.path.join(FEED_FOLDER, file_name)
    rows = []

    # Read the CSV and update the status of the matching title
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        for row in rows:
            if row[3] == title:  # Match based on title
                row[0] = status  # Update the "Read" status

    # Write the updated rows back to the CSV file
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)


# Function to handle the TUI menu using curses
def tui_menu(stdscr):
    # Set up color pairs
    curses.noecho()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Normal text
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Highlighted text
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)  # Error message

    # Get screen dimensions
    h, w = stdscr.getmaxyx()

    # Left and right panel dimensions
    left_w = w // 3  # 1/3rd for the left panel, rest for the right
    right_w = w - left_w

    # Find all CSV files
    csv_files = find_csv_files()
    selected_file_index = 0
    selected_row_index = 0
    csv_data = []

    while True:
        stdscr.clear()

        # Left panel: Display the available CSV files (feeds)
        stdscr.addstr(0, 0, "Feeds (CSV Files):", curses.color_pair(1))
        for idx, file in enumerate(csv_files):
            if idx == selected_file_index:
                stdscr.attron(curses.color_pair(2))  # Highlight selected file
                stdscr.addstr(idx + 1, 1, f"> {file[:left_w - 5]}")
                stdscr.attroff(curses.color_pair(2))
            else:
                stdscr.addstr(idx + 1, 1, f"  {file[:left_w - 5]}")

        # Right panel: Display the content of the selected feed (items in CSV)
        if csv_files:
            selected_file = csv_files[selected_file_index]
            csv_data = display_csv(selected_file)

            if isinstance(csv_data, str):  # In case of an error
                stdscr.addstr(1, left_w + 1, f"Error loading {selected_file}: {csv_data}", curses.color_pair(3))
            else:
                stdscr.addstr(0, left_w + 1, f"Items in {selected_file}:", curses.color_pair(1))
                headers = ["Date", "Title"]

                # Display headers (trim to fit right panel)
                for col_idx, header in enumerate(headers):
                    stdscr.addstr(1, left_w + 2 + col_idx * (right_w // len(headers)), header[:right_w // len(headers)],
                                  curses.color_pair(1))

                # Display rows
                for row_idx, row in enumerate(csv_data):  # Skip the header row of the CSV
                    display_row = "  ".join(row[1::2])  # Display only first 4 columns (Read, Date, Owner, Title)
                    if row_idx == selected_row_index:
                        stdscr.attron(curses.color_pair(2))  # Highlight selected row
                        stdscr.addstr(row_idx + 2, left_w + 1, display_row[:right_w - 2])
                        stdscr.attroff(curses.color_pair(2))
                    else:
                        if row[0].lower() != 'true':
                            stdscr.attron(curses.A_BOLD)
                            stdscr.addstr(row_idx + 2, left_w + 1, display_row[:right_w - 2])
                            stdscr.attroff(curses.A_BOLD)
                        else:
                            stdscr.addstr(row_idx + 2, left_w + 1, display_row[:right_w - 2])

        stdscr.refresh()

        # Handle user input
        key = stdscr.getch()
        if key == ord('q'):  # Quit program
            break
        elif key == curses.KEY_DOWN or key == ord('j'):
            if selected_file_index < len(csv_files) and not csv_data:
                selected_file_index += 1  # Move to next feed
            elif csv_data and selected_row_index < len(csv_data) - 1:
                selected_row_index += 1  # Move to next row in the feed
        elif key == curses.KEY_UP or key == ord('k'):
            if selected_file_index > 0 and not csv_data:
                selected_file_index -= 1  # Move to previous feed
            elif csv_data and selected_row_index > 0:
                selected_row_index -= 1  # Move to previous row in the feed
        elif key == ord('\n'):  # Enter key to open link
            if csv_data:
                link = csv_data[selected_row_index][4]  # Get link from the selected row (index +1 due to header)
                open_link(link)
        elif key == ord('r') and csv_data:
            # Mark the selected row as read
            csv_data[selected_row_index][0] = 'True'  # +1 due to header row
            update_csv(selected_file, csv_data[selected_row_index][3], 'True')


# Initialize curses and start the TUI
def main():
    curses.wrapper(tui_menu)


if __name__ == "__main__":
    main()
