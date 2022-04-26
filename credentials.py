import keyring

class CredentialsManager:

    def __init__(self):
        self.__system = "optext_service"
        keyring.get_keyring()
        self.credentials = []

    def check_username(self, username):
        ring = keyring.get_credential(self.__system, username)
        return ring is not None

    def check_password(self, username, password):
        ring = keyring.get_credential(self.__system, username)
        if ring and keyring.get_password(self.__system, username) == password:
            return True
        return False

    def create_credentials(self, username, password):
        keyring.set_password(self.__system, username, password)
        self.credentials.append(keyring.get_credential(self.__system, username))

    def delete_credentials(self):
        for cred in self.credentials:
            if cred.username and cred.password:
                keyring.delete_password(self.__system, cred.username)

