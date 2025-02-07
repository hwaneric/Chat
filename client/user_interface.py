import curses
import readline # Need to import readline to allow inputs to accept string with length > 1048
import sys
from client_socket import attempt_signup
sys.path.append('../')
from helpers.socket_io import read_socket, write_socket

def user_interface_driver(stdscr, client_sock):
    # curses.curs_set(0)  # Hide cursor
    # stdscr.keypad(1)  # Enable arrow keys
    # stdscr.clear()
    
    # options = ["Login", "Signup"]
    # current_option = 0

    welcome_screen(stdscr, client_sock)

    # while True:
    #     pass
        # stdscr.clear()
        # stdscr.addstr(0, 0, "Use ↑ ↓ to toggle, Enter to select", curses.A_BOLD)
        
        # for i, option in enumerate(options):
        #     if i == current_option:
        #         stdscr.addstr(i + 2, 2, f"> {option}", curses.A_REVERSE)  # Highlight currently selected option
        #     else:
        #         stdscr.addstr(i + 2, 2, f"  {option}")

        # key = stdscr.getch()

        # if key == curses.KEY_UP and current_option > 0:
        #     current_option -= 1
        # elif key == curses.KEY_DOWN and current_option < len(options) - 1:
        #     current_option += 1
        # elif key == ord("\n"):  # Enter key pressed
        #     stdscr.clear()

        #     match options[current_option]:
        #         case "Login":

        #             stdscr.addstr(2, 2, "Logging in...")
        #             stdscr.refresh()

        #             curses.napms(2000)  # Pause before next input
        #             # Implement login functionality here
        #         case "Signup":
        #             stdscr.clear()
        #             stdscr.refresh()

        #             # Implement signup functionality here
        #             signup_result = attempt_signup(client_sock)
        #             if signup_result["success"]:
        #                 stdscr.addstr(2, 2, signup_result["message"])
        #                 stdscr.refresh()
        #                 curses.napms(2000)
        #                 break
        #             else:
        #                 stdscr.addstr(2, 2, signup_result["message"])
        #                 stdscr.refresh()
        #                 curses.napms(2000)
        #         case _:
        #             stdscr.addstr(2, 2, "Invalid option. Please try again.")
        #             stdscr.refresh()
        #             curses.napms(2000)
        
        #     # stdscr.addstr(4, 2, f"You selected: {options[current_option]}", curses.A_BOLD)
        #     # stdscr.refresh()

def welcome_screen(stdscr, client_sock):
    curses.curs_set(0)  # Hide cursor
    stdscr.keypad(True)  # Enable arrow keys
    stdscr.clear()

    options = ["Login", "Signup"]
    current_option = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Use ↑ ↓ to toggle, Enter to select", curses.A_BOLD)

        # Render options
        for i, option in enumerate(options):
            if i == current_option:
                stdscr.addstr(i + 2, 2, f"> {option}", curses.A_REVERSE)  # Highlight currently selected option
            else:
                stdscr.addstr(i + 2, 2, f"  {option}")

        key = stdscr.getch()

        if key == curses.KEY_UP and current_option > 0:
            current_option -= 1
        elif key == curses.KEY_DOWN and current_option < len(options) - 1:
            current_option += 1
        elif key == ord("\n"):  # Enter key pressed
            stdscr.clear()

            match options[current_option]:
                case "Login":

                    stdscr.addstr(2, 2, "Logging in...")
                    stdscr.refresh()

                    curses.napms(2000)  # Pause before next input
                    # Implement login functionality here
                case "Signup":
                    stdscr.clear()
                    stdscr.refresh()

                    # Implement signup functionality here
                    signup_result = attempt_signup(client_sock)
                    if signup_result["success"]:
                        stdscr.addstr(2, 2, signup_result["message"])
                        stdscr.refresh()
                        curses.napms(2000)
                        break
                    else:
                        stdscr.addstr(2, 2, signup_result["message"])
                        stdscr.refresh()
                        curses.napms(2000)
                case _:
                    stdscr.addstr(2, 2, "Invalid option. Please try again.")
                    stdscr.refresh()
                    curses.napms(2000)

            # stdscr.addstr(4, 2, f"You selected: {options[current_option]}", curses.A_BOLD)
            # stdscr.refresh()
