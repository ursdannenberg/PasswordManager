#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
KeyGenerationKeyManager handles key generation keys.
"""

from preference_manager import PreferenceManager
from crypter import Crypter
from binascii import hexlify
import os


class KeyGenerationKeyManager(object):
    """
    New key generation key managers are uninitialized and either need a new key
    generation key or get one by decrypting an existing one.
    """
    def __init__(self):
        self.preference_manager = None
        self.key_generation_key = b""
        self.initialization_vector2 = None
        self.salt2 = None
        self.key_generation_key_crypter = None
        self.salt = b""

    def __str__(self):
        attr = ["Key generation key: " + str(hexlify(self.key_generation_key),
            encoding="utf-8"), "Salt: " + str(hexlify(self.salt),
            encoding="utf-8")]
        if self.initialization_vector2:
            attr.append("Initialization vector 2: " + str(hexlify(
                self.initialization_vector2), encoding="utf-8"))
        if self.salt2:
            attr.append("Salt 2: " + str(hexlify(self.salt2),
                encoding="utf-8"))
        return "<" + ", ".join(attr) + ">"

    def set_preference_manager(self, preference_manager):
        """
        Pass a preference manager to load and store settings.

        :param preference_manager: the preference manager
        :type preference_manager: PreferenceManager
        """
        if type(preference_manager) != PreferenceManager:
            raise TypeError
        self.preference_manager = preference_manager

    def get_salt(self):
        """
        Loads the salt. If there is none it is created and stored.

        :return: the salt
        :rtype: bytes
        """
        self.salt = self.preference_manager.get_salt()
        if len(self.salt) != 32:
            self.salt = Crypter.create_salt()
            self.store_salt(self.salt)
        return self.salt

    def store_salt(self, salt):
        """
        Stores the salt using the preference manager.

        :param salt: the salt
        :type salt: bytes
        """
        if type(salt) == bytes:
            self.salt = salt
            if self.preference_manager:
                self.preference_manager.store_salt(salt)
        else:
            raise TypeError("The salt to be saved is not of type byte.")

    def get_key_generation_key_crypter(self, password, salt):
        """
        Creates a key generation key crypter for the password and the salt.
        This is a computationally expensive operation.

        :param password: the password
        :type password: bytes
        :param salt: the salt
        :type salt: bytes
        :return: a key generation key crypter
        :rtype: Crypter
        """
        self.key_generation_key_crypter = Crypter(
            Crypter.create_key_initialization_vector(password = password,
            salt=salt))
        self.store_salt(salt = salt)
        return self.key_generation_key_crypter

    def create_new_key_generation_key(self):
        """
        Creates a new key generation key. This overwrites the previous one.

        :return: a new key generation key
        :rtype: bytes
        """
        self.key_generation_key = os.urandom(64)
        self.initialization_vector2 = Crypter.create_initialization_vector()
        self.salt2 = Crypter.create_salt()
        return self.key_generation_key

    def decrypt_key_generation_key(self, encrypted_key_generation_key,
        key_generation_key_crypter = None, password = b"", salt = b""):
        """
        Decrypts a key generation key. If a key generation key crypter is
        passed it is used. If none is passed a new key generation key crypter
        is created for the salt and the password. This is a computationally
        expensive operation. If the encrypted key generation key has a wrong
        length a new key generation key is created.

        :param encrypted_key_generation_key: the encrypted key generation key
        :type encrypted_key_generation_key: bytes
        :param key_generation_key_crypter: the key generation key crypter
        :type key_generation_key_crypter: Crypter
        :param password: the password
        :type password: bytes
        :param salt: the salt
        :type salt: bytes
        """
        if key_generation_key_crypter:
            self.key_generation_key_crypter = key_generation_key_crypter
        else:
            if len(salt) < 32:
                salt = Crypter.create_salt()
            self.get_key_generation_key_crypter(password, salt)
        if len(encrypted_key_generation_key) == 112:
            key_generation_key_block = \
                self.key_generation_key_crypter.decrypt_unpadded(
                encrypted_key_generation_key)
            self.salt2 = key_generation_key_block[:32]
            self.initialization_vector2 = key_generation_key_block[32:48]
            self.key_generation_key = key_generation_key_block[48:112]
        else:
            self.create_new_key_generation_key()

    def get_key_generation_key(self):
        """
        Returns the key generation key.

        :return: the key generation key
        :rtype: bytes
        """
        return self.key_generation_key

    def has_key_generation_key_crypter(self):
        """
        Returns true if there is a key generation key and a key generation key
        crypter.

        :return: key generation key and key generation key crypter?
        :rtype: bool
        """
        return self.key_generation_key and len(self.key_generation_key) == 64 \
            and self.key_generation_key_crypter

    def get_salt2(self):
        """
        Returns the salt 2.

        :return: salt 2
        :rtype: bytes
        """
        return self.salt2

    def get_initialization_vector2(self):
        """
        Returns the initialization vector 2.

        :return: initialization vector 2
        :rtype: bytes
        """
        return self.initialization_vector2

    def new_salt2(self):
        """
        Creates a new salt for the settings encryption (salt 2).
        """
        self.salt2 = Crypter.create_salt()

    def new_initialization_vector2(self):
        """
        Creates a new initialization vector for the settings encryption
        (initialization vector 2).
        """
        self.initialization_vector2 = Crypter.create_initialization_vector()

    def get_encrypted_key_generation_key_block(self):
        """
        Returns an encrypted key generation key block.

        :return: key generation key block
        :rtype: bytes
        """
        return self.key_generation_key_crypter.encrypt_unpadded(self.salt2 +
            self.initialization_vector2 + self.key_generation_key)

    def get_new_encrypted_key_generation_key_block(self):
        """
        Returns a encrypted key generation key block with a new salt 2 and a
        new initialization vector 2. This does not create a new key generation
        key.

        :return: key generation key block
        :rtype: bytes
        """
        self.new_initialization_vector2()
        self.new_salt2()
        return self.get_encrypted_key_generation_key_block()

    def create_and_store_new_key_generation_key_block_salt(self,
        key_generation_key_crypter = None):
        """
        Creates a new key generation key block and stores it.

        :param key_generation_key_crypter: the key generation key crypter
        :type key_generation_key_crypter: Crypter
        :return: key generation key block
        :rtype: bytes
        """
        self.salt = Crypter.create_salt()
        self.store_salt(self.salt)
        if key_generation_key_crypter:
            self.key_generation_key_crypter = key_generation_key_crypter
        key_generation_key_block = \
            self.get_new_encrypted_key_generation_key_block()
        self.preference_manager.store_key_generation_key_block(
            key_generation_key_block)
        return key_generation_key_block

    def store_key_generation_key_block_salt(self):
        """
        Stores the key generation key block.
        """
        if self.preference_manager:
            self.preference_manager.store_key_generation_key_block(
                self.get_encrypted_key_generation_key_block())
        if len(self.salt) == 32:
            self.store_salt(self.salt)
        else:
            raise ValueError("The salt must be 32 bytes long.")

    def reset(self):
        """
        Resets the key generation key manager.
        """
        self.salt = b""
        self.initialization_vector2 = None
        self.salt2 = None
        self.key_generation_key = b""
        self.key_generation_key_crypter = None
