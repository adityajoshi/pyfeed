import curses

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()

    # Starting position
    x = 0
    y = 0

    # Set up a simple loop to capture user input
    while True:
        stdscr.clear()
        stdscr.addstr(y, x, 'O')  # Display 'O' as the cursor

        key = stdscr.getch()

        if key == curses.KEY_UP:
            y = max(y - 1, 0)
        elif key == curses.KEY_DOWN:
            y = min(y + 1, curses.LINES - 1)
        elif key == curses.KEY_LEFT:
            x = max(x - 1, 0)
        elif key == curses.KEY_RIGHT:
            x = min(x + 1, curses.COLS - 1)
        elif key == ord('q'):
            break  # Press 'q' to quit

        stdscr.refresh()

curses.wrapper(main)
