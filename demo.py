import curses

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # Print a message in the middle of the screen
    height, width = stdscr.getmaxyx()
    message = "Hello, curses!"
    x = width // 2 - len(message) // 2
    y = height // 2
    stdscr.addstr(y, x, message)

    # Refresh the screen
    stdscr.refresh()

    # Wait for user input
    stdscr.getch()

curses.wrapper(main)
