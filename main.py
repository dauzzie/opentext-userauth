from credentials import CredentialsManager
from menu import Menu
import os

def main():
    credManager = CredentialsManager()
    win_file = "DO_NOT_DELETE_win_data_temp"
    try:
        this_menu = Menu(credManager)
    except Exception as e:
        print("error occured:", e)
    finally:
        credManager.delete_credentials()
        if os.path.exists(win_file):
            os.remove(win_file)

if __name__ == '__main__':
    main()