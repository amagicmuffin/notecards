import curses
import textwrap

def draw_menu(stdscr):
    # Clear and refresh the screen for a blank canvas
    stdscr.erase()
    stdscr.refresh()

    # Loop where k is the last character pressed
    k = 0
    while (k != ord('q')):

        # Initialization
        stdscr.erase()

        if k == curses.KEY_DOWN:
            stdscr.addstr(1, 0, "pressed")
        elif k == curses.KEY_UP:
            stdscr.addstr(1, 0, "pressed")
        elif k == curses.KEY_RIGHT:
            stdscr.addstr(1, 0, "pressed")
        elif k == curses.KEY_LEFT:
            stdscr.addstr(1, 0, "pressed")


        # Rendering some text
        stdscr.addstr(0, 0, "test")

        


        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

s = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. \n\nPraesent vitae massa justo. Quisque lacinia suscipit ante. Morbi sit amet tortor ut purus vulputate ullamcorper quis ut arcu. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam non augue dictum, mattis neque ac, eleifend sapien. Curabitur interdum sollicitudin nulla nec consequat. Suspendisse imperdiet sagittis justo et sodales. Vivamus congue tincidunt tortor nec dictum. Proin a mauris ut eros fermentum fermentum.\n\n\n\n Suspendisse nec mi et tortor ultrices pulvinar. Duis erat quam, laoreet ut dui a, cursus elementum est. Vivamus ut venenatis felis, malesuada ultrices arcu. Mauris urna justo, faucibus non lobortis sed, interdum in diam. Curabitur eu purus at quam lacinia elementum in et lacus."

def main():
    # curses.wrapper(draw_menu)
    # print(textwrap.fill(s, replace_whitespace=False))
    raise Exception("Date provided can't be in the past")

if __name__ == "__main__":
    main()

