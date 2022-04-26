from threading import local
from unittest import TestCase
import unittest
import os
from credentials import CredentialsManager
import keyring
from random_username.generate import generate_username
import random

cred = CredentialsManager()

def generate_random_username():
    return generate_username(1)

local_username = generate_random_username()[0]
local_password = generate_random_username()[0]


class CredentialsTest(TestCase):

    def test_keyring(self):
        ring = keyring.get_keyring()
        assert ring is not None

    def test_credentials_exist(self):
        cred.delete_credentials()
        cred.create_credentials(local_username, local_password)
        assert cred.check_username(local_username) is True and cred.check_password(local_username, local_password) is True

    def test_password_not_match(self):
        cred.delete_credentials()
        cred.create_credentials(local_username, local_password)
        new_password = generate_random_username()[0]
        while new_password == local_password:
            new_password = generate_random_username()[0]
        assert cred.check_password(local_username, new_password) is False

if __name__ == '__main__':
    unittest.main()