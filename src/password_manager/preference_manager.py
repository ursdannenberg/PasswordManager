#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
PreferenceManager handles the access to the settings file.
"""
import os

PASSWORD_SETTINGS_FILE = os.path.expanduser("~/.passwords")


class PreferenceManager(object):
    def __init__(self, settings_file = PASSWORD_SETTINGS_FILE):
        """
        :param settings_file: Filename of the settings file.
            Defaults to ~/.passwords.
        :type settings_file: str
        """
        self.data = b""
        self.settings_file = settings_file
        self.read_file()

    def read_file(self):
        """
        Reads the settings file.
        """
        if os.path.isfile(self.settings_file):
            with open(self.settings_file, "rb") as file:
                self.data = file.read()

    def get_salt(self):
        """
        Reads the salt.

        :return: the salt
        :rtype: bytes
        """
        return self.data[:32]

    def store_salt(self, salt):
        """
        Writes the salt to the first 32 bytes of the settings file.

        :param salt: the salt
        :type salt: bytes
        """
        if type(salt) != bytes:
            raise TypeError("The salt must be of type byte.")
        if len(salt) != 32:
            raise ValueError("The salt must be 32 bytes long.")
        if os.path.isfile(self.settings_file):
            with open(self.settings_file, "rb+") as file:
                file.seek(0)
                file.write(salt)
        else:
            with open(self.settings_file, "wb") as file:
                file.write(salt)
        self.data = salt + self.data[32:]

    def get_key_generation_key_block(self):
        """
        Reads the key generation key block.

        :return: key generation key block
        :rtype: bytes
        """
        return self.data[32:144]

    def store_key_generation_key_block(self, key_generation_key_block):
        """
        Writes the key generation key block to the bytes 32 to 143 of the
        settings file.

        :param key_generation_key_block: the encrypted key generation key block
        :type key_generation_key_block: bytes
        """
        if type(key_generation_key_block) != bytes:
            raise TypeError("The key generation key block must be of type " +
                "byte.")
        if len(key_generation_key_block) != 112:
            raise ValueError("The key generation key block must be 112 bytes "
                + "long.")
        if os.path.isfile(self.settings_file):
            with open(self.settings_file, "rb+") as file:
                file.seek(32)
                file.write(key_generation_key_block)
        else:
            with open(self.settings_file, "wb") as file:
                file.write(b"\x00" * 32)
                file.write(key_generation_key_block)
        self.data = self.data[:32] + key_generation_key_block + self.data[144:]

    def get_settings_data(self):
        """
        Reads the encrypted settings data.

        :return: encrypted settings data
        :rtype: bytes
        """
        return self.data[144:]

    def store_settings_data(self, settings_data):
        """
        Writes the encrypted settings data to the bytes beginning with byte 144
        of the settings file.

        :param settings_data: encrypted settings data
        :type settings_data: bytes
        """
        if type(settings_data) != bytes:
            raise TypeError("The settings data must be of type byte.")
        if os.path.isfile(self.settings_file):
            with open(self.settings_file, "rb+") as file:
                file.seek(144)
                file.write(settings_data)
                file.truncate()
        else:
            with open(self.settings_file, "wb") as file:
                file.write(b"\x00" * 144)
                file.write(settings_data)
        self.data = self.data[:144] + settings_data
