#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
SettingsManager handles the settings for all domains.
"""

import json
import struct
from datetime import datetime
from setting import Setting
from crypter import Crypter
from packer import Packer
from base64 import b64decode, b64encode
from key_generation_key_manager import KeyGenerationKeyManager


class SettingsManager(object):
    def __init__(self, preference_manager):
        self.preference_manager = preference_manager
        self.settings = []

    @staticmethod
    def get_settings_crypter(key_generation_key_manager):
        """
        Creates a crypter for the settings.

        :param key_generation_key_manager: the key generation key manager
        :type key_generation_key_manager: KeyGenerationKeyManager
        :return: Crypter for settings
        :rtype: Crypter
        """
        return Crypter(Crypter.create_key(
            key_generation_key_manager.get_key_generation_key(),
            key_generation_key_manager.get_salt2()) +
            key_generation_key_manager.get_initialization_vector2())

    def load_settings(self, key_generation_key_manager):
        """
        Loads the settings for all domains from the hard drive.

        :param key_generation_key_manager: the key generation key manager
        :type key_generation_key_manager: KeyGenerationKeyManager
        """
        encrypted_settings = self.preference_manager.get_settings_data()
        if len(encrypted_settings) < 40:
            return
        settings_crypter = SettingsManager.get_settings_crypter(
            key_generation_key_manager)
        decrypted_settings = settings_crypter.decrypt(encrypted_settings)
        try:
            decompressed_settings = Packer.decompress(decrypted_settings[4:])
        except ValueError:
            raise PermissionError("Wrong master password: The settings could "
                + "not be decompressed.")
        settings_len = struct.unpack("!I", decrypted_settings[0:4])[0]
        saved_settings = json.loads(str(decompressed_settings,
            encoding="utf-8"))
        if len(saved_settings) < settings_len:
            raise ValueError("The decrypted settings are too short to be " +
                "decompressed.")
        for domain_name in saved_settings.keys():
            data_set = saved_settings[domain_name]
            found = False
            i = 0
            while i < len(self.settings):
                setting = self.settings[i]
                if setting.get_domain() == domain_name:
                    found = True
                    if datetime.strptime(data_set["mDate"],
                        "%Y-%m-%dT%H:%M:%S") > setting.get_m_date():
                        setting.load_from_dict(data_set)
                i += 1
            if not found:
                new_setting = Setting(domain_name)
                new_setting.load_from_dict(data_set)
                self.settings.append(new_setting)

    def store_settings(self, key_generation_key_manager):
        """
        Stores the settings for all domains on the hard drive.

        :param key_generation_key_manager: the key generation key manager
        :type key_generation_key_manager: KeyGenerationKeyManager
        """
        key_generation_key_manager.new_salt2()
        key_generation_key_manager.new_initialization_vector2()
        settings_crypter = SettingsManager.get_settings_crypter(
            key_generation_key_manager)
        self.preference_manager.store_settings_data(settings_crypter.encrypt(
            struct.pack('!I', len(self.get_settings_as_dict())) +
            Packer.compress(json.dumps(self.get_settings_as_dict()))))
        key_generation_key_manager.store_key_generation_key_block_salt()

    def get_setting(self, domain):
        """
        Returns the settings for the domain. If no settings are stored new
        settings are created.

        :param domain: the domain name
        :type domain: str
        :return: the settings
        :rtype: Setting
        """
        for setting in self.settings:
            if setting.get_domain() == domain:
                return setting
        setting = Setting(domain)
        self.settings.append(setting)
        return setting

    def set_setting(self, setting):
        """
        Stores the settings for a domain in the RAM. Call store_settings to
        store them on the hard drive.

        :param setting: the settings
        :type setting: Setting
        """
        for i, existing_setting in enumerate(self.settings):
            if existing_setting.get_domain() == setting.get_domain():
                self.settings.pop(i)
        self.settings.append(setting)

    def delete_setting(self, setting):
        """
        Removes the settings for a domain from the RAM.

        :param setting: the settings
        :type setting: Setting
        """
        i = 0
        while i < len(self.settings):
            existing_setting = self.settings[i]
            if existing_setting.get_domain() == setting.get_domain():
                self.settings.pop(i)
            else:
                i += 1

    def get_domain_list(self):
        """
        Returns a list of the domain names.

        :return: the list of domain names
        :rtype: [str]
        """
        return [setting.get_domain() for setting in self.settings]

    def get_settings_as_dict(self):
        """
        Returns a dictionary with the list of settings.

        :return: the dictionary with the list of settings
        :rtype: dict
        """
        settings_dict = {}
        for setting in self.settings:
            settings_dict[setting.get_domain()] = setting.to_dict()
        return settings_dict
