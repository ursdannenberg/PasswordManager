#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Crypter handles the encryption and the decryption with AES in CBC mode with
PKCS7 padding and the creation of keys, initialization vectors, and salts.
"""

from Crypto.Cipher import AES
from hashlib import pbkdf2_hmac
import os


class Crypter(object):
    def __init__(self, key_initialization_vector):
        if len(key_initialization_vector) == 48:
            self.key = key_initialization_vector[:32]
            self.initialization_vector = key_initialization_vector[32:]
        else:
            raise ValueError("Wrong length of the key and the initialization "
                + "vector.")

    @staticmethod
    def create_key(password, salt, iterations = 1024):
        """
        Creates a key for encrypting or decrypting the settings for all domains.

        :param password: the KGK
        :type password: bytes
        :param salt: the salt 2
        :type salt: bytes
        :param iterations: the iteration count
        :type iterations: int
        :return: the key
        :rtype: bytes
        """
        return pbkdf2_hmac("sha256", password, salt, iterations)

    @staticmethod
    def create_key_initialization_vector(password, salt, iterations = 32768):
        """
        Creates a key and an initialization vector for key generation key
        crypters.

        :param password: the key generation key
        :type password: bytes
        :param salt: the salt 2
        :type salt: bytes
        :param iterations: the iteration count
        :type iterations: int
        :return: the key and the initialization vector
        :rtype: bytes
        """
        return pbkdf2_hmac("sha384", password, salt, iterations)

    @staticmethod
    def create_salt():
        """
        Create a new salt with 32 bytes.

        :return: the salt
        :rtype: bytes
        """
        return os.urandom(32)

    @staticmethod
    def create_initialization_vector():
        """
        Create a new initialization vector with 16 bytes.

        :return: the initialization vector
        :rtype: bytes
        """
        return os.urandom(16)

    @staticmethod
    def add_pkcs7_padding(data):
        """
        Adds PKCS7 padding to the data so they can be divided into blocks of
        16 bytes.

        :param data: the data without padding
        :type data: bytes
        :return: the data with padding
        :rtype: bytes
        """
        length = 16 - (len(data) % 16)
        data += bytes([length]) * length
        return data

    def encrypt(self, data):
        """
        Encrypts the data with AES in CBC mode with PKCS7 padding.

        :param data: the unencrypted data
        :type data: bytes
        :return: the encrypted data
        :rtype: bytes
        """
        aes_object = AES.new(self.key, AES.MODE_CBC, self.initialization_vector)
        return aes_object.encrypt(self.add_pkcs7_padding(data))

    def encrypt_unpadded(self, data):
        """
        Encrypts the data with AES in CBC mode without padding. The data has to
        fit into blocks of 16 bytes.

        :param data: the unencrypted data
        :type data: bytes
        :return: the encrypted data
        :rtype: bytes
        """
        aes_object = AES.new(self.key, AES.MODE_CBC, self.initialization_vector)
        return aes_object.encrypt(data)

    @staticmethod
    def remove_pkcs7_padding(data):
        """
        Removes the PKCS7 padding.

        :param data: the data with padding
        :type data: bytes
        :return: the data without padding
        :rtype: bytes
        """
        return data[:-data[-1]]

    def decrypt(self, encrypted_data):
        """
        Decrypts the data with AES in CBC mode with PKCS7 padding.

        :param encrypted_data: the encrypted data
        :type encrypted_data: bytes
        :return: the decrypted data
        :rtype: bytes
        """
        aes_object = AES.new(self.key, AES.MODE_CBC, self.initialization_vector)
        return self.remove_pkcs7_padding(aes_object.decrypt(encrypted_data))

    def decrypt_unpadded(self, encrypted_data):
        """
        Decrypts the data with AES in CBC mode without padding. The data has to
        fit into blocks of 16 bytes.

        :param encrypted_data: the encrypted data
        :type encrypted_data: bytes
        :return: the decrypted data
        :rtype: bytes
        """
        aes_object = AES.new(self.key, AES.MODE_CBC, self.initialization_vector)
        return aes_object.decrypt(encrypted_data)
