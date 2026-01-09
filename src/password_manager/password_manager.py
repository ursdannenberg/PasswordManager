#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Main file for PasswordManager.
"""

from password_generator import PasswordGenerator
from preference_manager import PreferenceManager
from key_generation_key_manager import KeyGenerationKeyManager
from settings_manager import SettingsManager
from auto_completer import AutoCompleter
from datetime import datetime
import argparse
import getpass
import readline
import sys
import pyperclip
from termcolor import colored

def create_settings_manager(key_generation_key_manager, master_password):
    """
    Creates the settings manager.
    :param key_generation_key_manager: the key generation key manager
    :type key_generation_key_manager: KeyGenerationKeyManager
    """
    preference_manager = PreferenceManager()
    key_generation_key_manager.set_preference_manager(preference_manager)
    key_generation_key_manager.decrypt_key_generation_key(
        preference_manager.get_key_generation_key_block(),
        password = master_password.encode("utf-8"),
        salt = preference_manager.get_salt())
    return SettingsManager(preference_manager), preference_manager

def has_setting(domain):
    """
    Returns the domain name and True if settings for the domain are stored.
    
    :param domain: the domain name
    :type domain: str
    """
    setting_found = False
    if domain in settings_manager.get_domain_list():
        setting_found = True
    else:
        for dom in settings_manager.get_domain_list():
            if dom[:len(domain)] == domain:
                print('For "' + dom + '" settings were found.')
                answer = input("Load settings? [y/n] ")
                if answer not in ["n", "N", "no", "No", "NO", "not", "Not",
                    "NOT", "nay", "Nay", "NAY", "nein", "Nein", "NEIN"]:
                    domain = dom
                    setting_found = True
    return domain, setting_found

def get_username(setting, option):
    """
    Copies the username for the domain to the clipboard if "1" is passed as
    option or displays it if "2" is passed.
    
    :param setting: the settings for the domain
    :type setting: Setting
    :param option: "1" or "2"
    :type option: string
    """
    if option == "1":
        pyperclip.copy(setting.get_username())
        print("The username was copied to the clipboard.")
        input("Press any key to copy the password to the clipboard.")
    else:
        print("Username: " + setting.get_username())

def get_fixed_password(setting, option):
    """
    Copies the fixed password for the domain to the clipboard if "1" is passed
    as option or displays it if "2" is passed.
    
    :param setting: the settings for the domain
    :type setting: Setting
    :param option: "1" or "2"
    :type option: string
    """
    if option == "1":
        pyperclip.copy(setting.get_fixed_password())
        print("The password was copied to the clipboard.")
    else:
        colored_password = color_password(setting.get_fixed_password())
        print("Fixed password: " + colored_password)


def get_generated_password(setting, key_generation_key, option):
    """
    Generates and copies the generated password for the domain to the clipboard
    if "1" is passed as option or displays it if "2" is passed.
        
    :param setting: the settings for the domain
    :type setting: Setting
    :param key_generation_key: the key generation key
    :type key_generation_key: bytes
    :param option: "1" or "2"
    :type option: string
    """
    password_generator = PasswordGenerator(setting.get_domain(),
        key_generation_key, setting.get_salt(), setting.get_iterations())
    password = password_generator.generate(setting)
    if option == "1":
        pyperclip.copy(password)
        print("The password was copied to the clipboard.")
    else:
        colored_password = color_password(password)
        print("Generated password: " + colored_password)

def color_password(password):
    """
    Colors the password before displaying. Digits are printed in blue,
    lower-case letters in green, upper-case letters in red,
    and special characters in yellow.
        
    :param password: the password to be colored
    :type setting: string
    """    
    colored_password = ''
    for char in password:
        if char.isdigit():
            colored_password += colored(char, 'blue')
        elif char.islower():
            colored_password += colored(char, 'green')
        elif char.isupper():
            colored_password += colored(char, 'red') 
        else:
            colored_password += colored(char, 'yellow')
    return  colored_password
        
def get_password(setting, key_generation_key, option):
    """
    Copies the username and the password for the domain to the clipboard
    or displays them.
        
    :param setting: the settings for the domain
    :type setting: Setting
    :param key_generation_key: the key generation key
    :type key_generation_key: bytes
    :param option: "1" or "2"
    :type option: string
    """
    if setting.has_username():
        get_username(setting, option)
    else:
        print("Username is not set.")
    if setting.has_fixed_password():
        get_fixed_password(setting, option)
    else:
        get_generated_password(setting, key_generation_key, option)
    input("Press any key to continue.")

def setting_menu(setting, key_generation_key_manager, settings_manager):
    """
    Menu to access, change, and delete the settings for the domain.
        
    :param setting: the settings for the domain
    :type setting: Setting
    :param key_generation_key_manager: the key generation key manager
    :type key_generation_key_manager: KeyGenerationKeyManager
    :param settings_manager: the settings manager
    :type settings_manager: SettingsManager
    """
    while True:
        option = input("Choose one of the following options:"
            + "\n1\tcopy username and password to clipboard"
            + "\n2\tdisplay username and password"
            + "\n3\tdisplay settings except for password\n4\tchange settings"
            + "\n5\tdelete domain\n6\treturn to previous menu\n[1/2/3/4/5/6] ")
        while option not in ["1", "2", "3", "4", "5", "6"]:
            option = input('Enter "1", "2", "3", "4", "5", or "6": ')
        if option in ["1", "2"]:
            get_password(setting,
                key_generation_key_manager.get_key_generation_key(), option)
        elif option == "3":
            setting.get_settings()
        elif option == "4":
            if setting.has_fixed_password():
                setting.set_settings_menu_fixed_password()
            else:
                setting.set_settings_menu_generated_password()
            settings_manager.set_setting(setting)
            setting.set_modification_date(datetime.now())
            settings_manager.store_settings(key_generation_key_manager)
        elif option == "5":
            answer = input("Are you sure you want to delete the domain? [y/n] ")
            if answer not in ["n", "N", "no", "No", "NO", "not", "Not", "NOT",
                "nay", "Nay", "NAY", "nein", "Nein", "NEIN"]:
                settings_manager.delete_setting(setting)
                settings_manager.store_settings(key_generation_key_manager)
                input("The domain was deleted. Press any key to continue.")
                break
        else:
            break
