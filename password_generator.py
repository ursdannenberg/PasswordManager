#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
PasswordGenerator generates passwords from the master password and the domain
name.
"""

from crypter import Crypter
from hashlib import pbkdf2_hmac

class PasswordGenerator(object):
    """
    Salt defaults to a randomly generated salt, iteration count to 4096.

    :param domain: the domain
    :type domain: str
    :param key_generation_key: the key generation key
    :type key_generation_key: bytes
    :param salt: the salt
    :type salt: bytes
    :param iterations: the iteration count
    :type iterations: int
    """
    def __init__(self, domain, key_generation_key,
        salt = Crypter.create_salt(), iterations = 4096):
        start_value = b""
        for value in domain.encode("utf-8"):
            start_value += bytes([value])
        for value in key_generation_key:
            start_value += bytes([value])
        if iterations < 1:
            print("Desired number of iterations was below 1." +
                "Using 4096 iterations instead.")
            iterations = 4096
        self.hash_value = pbkdf2_hmac("sha512", start_value, salt, iterations)

    def generate(self, setting):
        """
        Generates a password.

        :param password_setting: the settings
        :type password_setting: Setting
        :return: password
        :rtype: str
        """
        number = int.from_bytes(self.hash_value, byteorder = "big")
        password = ""
        character_set = setting.get_character_set()
        digits_set = setting.get_digits_character_set()
        lower_set = setting.get_lower_case_character_set()
        upper_set = setting.get_upper_case_character_set()
        extra_set = setting.get_extra_character_set()
        template = setting.get_template()
        for value in template:
            if number > 0:
                if value == "a":
                    current_set = lower_set
                elif value == "A":
                    current_set = upper_set
                elif value == "n":
                    current_set = digits_set
                elif value == "o":
                    current_set = extra_set
                else:
                    current_set = character_set
                if len(current_set) > 0:
                    password = password + current_set[number % len(current_set)]
                    number //= len(current_set)
        return password
