
from enum import Enum
import curses
import getpass
import os

class MenuMode(Enum):
    MAIN = 1
    LOGGED_IN = 2

class MainMode(Enum):
    MENU = 1
    LOGIN = 2
    SIGNUP = 3

class Menu:

    def __init__(self, credManager):
        self.menumode = MenuMode.MAIN
        self.mainmode = MainMode.MENU
        self.__menu = ['Login', 'Register', 'Quit', 'Logout']
        self.curr_menu = self.__menu
        self.curr_user = ""
        self.save_file = "DO_NOT_DELETE_win_data_temp"
        self.credManager = credManager
        curses.wrapper(self.main)

    def main(self, stdscr):
        curses.curs_set(0)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # set screen object as class property
        self.stdscr = stdscr

        # get screen height and width
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()
        self.center_pos = (self.screen_height // 2, self.screen_width // 2)

        curr_idx = 0

        while True:
            self.stdscr.clear()
            self.update_menu()
            print(self.curr_menu)
            self.print_menu(curr_idx)
            key = self.stdscr.getch()

            if key == curses.KEY_UP and curr_idx > 0:
                curr_idx -= 1
            elif key == curses.KEY_DOWN and curr_idx < len(self.curr_menu) - 1:
                curr_idx += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                # if user selected last row (Exit), confirm before exit the program
                if curr_idx == len(self.curr_menu) - 1:
                    if self.confirm("Are you sure you want to exit?"):
                        break
                else:
                    self.navigate(self.curr_menu[curr_idx])
                    curr_idx = 0
            self.stdscr.refresh()

    def navigate(self, item):
        if item == 'Login':
            self.login(self.credManager)
        elif item == 'Register':
            self.register(self.credManager)
        elif item == 'Logout':
            self.curr_user = None
            self.print_center("Logging out...")
            y, _ = self.center_pos
            self.pause(y+1)
            self.update_menu()

    def update_menu(self):
        if self.menumode == MenuMode.MAIN and self.curr_user:
            self.curr_menu = list(reversed(self.__menu[-2:]))
            self.curr_menu = [self.curr_user] + self.curr_menu
        else:
            self.curr_menu = self.__menu[:-1]
            self.curr_user = ""
        print(self.menumode)

    def print_menu(self, curr_idx=0):
        self.stdscr.clear()
        for idx, row in enumerate(self.curr_menu):
            x = self.screen_width // 2 - len(row) // 2
            y = self.screen_height // 2 - len(self.curr_menu) // 2 + idx
            if idx == curr_idx:
                self.color_print(y, x, row, 1)
            else:
                self.stdscr.addstr(y, x, row)
        self.stdscr.refresh()


    #region Confirm

    def print_confirm(self, selected="yes"):
        # clear yes/no line
        curses.setsyx(self.screen_height // 2 + 1, 0)
        self.stdscr.clrtoeol()

        y = self.screen_height // 2 + 1
        options_width = 10

        # print yes
        option = "yes"
        x = self.screen_width // 2 - options_width // 2 + len(option)
        if selected == option:
            self.color_print(y, x, option, 1)
        else:
            self.stdscr.addstr(y, x, option)

        # print no
        option = "no"
        x = self.screen_width // 2 + options_width // 2 - len(option)
        if selected == option:
            self.color_print(y, x, option, 1)
        else:
            self.stdscr.addstr(y, x, option)

        self.stdscr.refresh()

    def confirm(self, confirmation_text):
        self.print_center(confirmation_text)

        current_option = "yes"
        self.print_confirm(current_option)

        while True:
            key = self.stdscr.getch()

            if key == curses.KEY_RIGHT and current_option == "yes":
                current_option = "no"
            elif key == curses.KEY_LEFT and current_option == "no":
                current_option = "yes"
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return True if current_option == "yes" else False

            self.print_confirm(current_option)


    #endregion

    #region Helper functions
    def color_print(self, y, x, text, pair_num):
        self.stdscr.attron(curses.color_pair(pair_num))
        self.stdscr.addstr(y, x, text)
        self.stdscr.attroff(curses.color_pair(pair_num))

    def print_center(self, text):
        self.stdscr.clear()
        x = self.screen_width // 2 - len(text) // 2
        y = self.screen_height // 2
        self.stdscr.addstr(y, x, text)
        self.stdscr.refresh()

    def save_window(self):

        with open(self.save_file, 'wb') as f:
            self.stdscr.putwin(f)

    def retrieve_window(self):
        self.stdscr.clear()
        with open(self.save_file, 'rb') as f:
            self.stdscr = curses.getwin(f)
        self.stdscr.refresh()
        os.remove(self.save_file)

    def pause(self, y):
        _, x = self.center_pos
        while True:
            text = "Press any key to continue..."
            local_x = x - len(text) // 2
            self.stdscr.addstr(y, local_x, text)
            key = self.stdscr.getch()

            if key:
                break

    #endregion

    #region Input Handlers

    def handle_input_errors(self, errors):
        self.stdscr.clear()
        y, x = self.center_pos
        for i, text in enumerate(errors):
            local_x = x - len(text) // 2
            self.stdscr.addstr(y+i, local_x, text)
        self.pause(y+i+1)
        self.stdscr.refresh()

    def text_input(self, line, cursor, is_login=False, flag=False):

        result_str = ""
        if flag:
            curses.noecho()
        else:
            curses.echo()

        while True:
            if not flag:

                self.stdscr.move(line, cursor)
                self.stdscr.clrtoeol()
                self.stdscr.addstr(result_str)

            key = self.stdscr.getch()

            if str(key) in ('KEY_BACKSPACE', '\b', '\x7f', '^?') or key == 127:
                if result_str:
                    result_str = result_str[:-1]
            elif key == curses.KEY_ENTER or key in [10,13]:
                return (result_str, self.valid_entry(result_str, flag))
            elif key == 27 or str(key) in ('^['):
                return "", ["ESCAPE"]
            else:
                ch = chr(key)
                if ch.isprintable():
                    result_str += ch
            self.stdscr.refresh()

    def valid_entry(self, result_str, flag=False):
        # rules: username and password both alphanumeric, 5-45 chars
        errors = []
        if any(not s.isalnum() for s in result_str):
            errors.append("Usernames/Passwords must be consisting only alphanumeric characters")
        if len(result_str) < 5 or len(result_str) > 45:
            errors.append("Usernames/Passwords must be of length 5-45")

        return errors

    #endregion

#region Routes
    def login(self, credManager):
        # Username and password

        y, x = self.center_pos
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(y, x, "Username: ")
            _, x = self.stdscr.getyx()
            username, errors = (self.text_input(y, x+1, True, False))
            self.stdscr.refresh()
            if errors:
                if "ESCAPE" in errors:
                    return
                self.handle_input_errors(errors)
            elif not credManager.check_username(username):
                self.handle_input_errors(["Username doesn't exist"])
            else:
                break
        y += 1

        _, x = self.center_pos
        self.stdscr.addstr(y, x, "Password: ")
        _, x = self.stdscr.getyx()
        while True:
            self.save_window()
            password, errors = self.text_input(y, x+1, False, True)
            if errors:
                if "ESCAPE" in errors:
                    return
                self.handle_input_errors(errors)
                self.retrieve_window()
            elif not credManager.check_password(username, password):
                self.handle_input_errors(["Incorrect password"])
                self.retrieve_window()
            else:
                break
        self.curr_user = username
        self.update_menu()
        return


    def register(self, credManager):
        y, x = self.center_pos
        while True:
            y, x = self.center_pos
            self.stdscr.clear()
            self.stdscr.addstr(y, x, "Username: ")
            _, x = self.stdscr.getyx()
            username, errors = self.text_input(y, x+1, False, False)
            self.stdscr.refresh()
            if errors:
                if "ESCAPE" in errors:
                    return
                self.handle_input_errors(errors)
            elif credManager.check_username(username):
                self.handle_input_errors(["Username already exists"])
            else:
                break
        y += 1

        _, x = self.center_pos
        self.stdscr.addstr(y, x, "Password: ")
        _, x = self.stdscr.getyx()
        while True:
            self.save_window()
            password, errors = self.text_input(y, x+1, False, True)
            if errors:
                if "ESCAPE" in errors:
                    return
                self.handle_input_errors(errors)
                self.retrieve_window()
            else:
                break
        credManager.create_credentials(username, password)
        self.menumode = MenuMode.LOGGED_IN
        print(username)
        self.update_menu(username)


#endregion Routes