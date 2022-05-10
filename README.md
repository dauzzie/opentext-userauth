OpenText Userauth

A user authentication program using Keyring as credentials mechanic. More info on: https://keyring.readthedocs.io/en/latest/

Installations:

1. Clone this repository
2. Make sure using Python version `3.9.10` or later
3. Run `pip install -r requirements.txt`
4. Run `python3 main.py`

Information:

- Usernames and passwords would be only alphanumeric and length between 5-45 characters
- Keyring stores credentials on Keychain (MacOS), secretstorage (Linux), and Windows Credential Locker(Windows)


Project Structure:
1. `main.py` - Main file class.
2. `menu.py` - Used python's curses to generate UI on screen.
   1. Use up, down, left, right keys to navigate menu
   2. Press esc to return to menu
3. `credentials.py` - Credentials file class


