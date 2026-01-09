#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Setting handles the settings for a domain.
"""

from crypter import Crypter
from datetime import datetime
import getpass
import string
import re
import binascii
from base64 import b64encode, b64decode
from random import shuffle

DEFAULT_LOWER_CASE_CHARACTERS = string.ascii_lowercase
DEFAULT_UPPER_CASE_CHARACTERS = string.ascii_uppercase
DEFAULT_DIGITS = string.digits
DEFAULT_EXTRA_CHARACTERS = '#!"§$%&/()[]{}=-_+*<>;:.'


class Setting(object):
    def __init__(self, domain):
        self.domain = domain
        self.username = None
        self.fixed_password = None
        self.url = None
        self.notes = None
        self.length = 16
        self.iterations = 4096
        self.salt = Crypter.create_salt()
        self.creation_date = datetime.now()
        self.modification_date = self.creation_date
        self.extra_characters = DEFAULT_EXTRA_CHARACTERS
        self.template = "x"*16
        self.calculate_template(True, True, True, True)

    def __str__(self):
        output = "<" + self.domain + ": ("
        if self.username:
            output += "username: " + str(self.username) + ", "
        if self.fixed_password:
            output += "fixed password: " + str(self.fixed_password) + ", "
        output += "password length: " + str(self.length) + ", "
        output += "extra character set: \"" + self.extra_characters + "\", "
        output += "iteration count: " + str(self.iterations) + ", "
        output += "salt: " + str(binascii.hexlify(self.salt)) + ", "
        output += "template: " + str(self.template) + ", "
        if self.notes:
            output += "URL: " + str(self.url) + ", "
        if self.notes:
            output += "notes: " + str(self.notes) + ", "
        output += "modification date: " + self.get_modification_date() + ", "
        output += "creation date: " + self.get_creation_date() + ", "
        output += ")>"
        return output

    def get_domain(self):
        """
        Returns the domain name.

        :return: the domain name
        :rtype: str
        """
        return self.domain

    def set_domain(self, domain):
        """
        Sets the domain name.

        :param domain: a domain name
        :type domain: str
        """
        self.domain = domain

    def change_domain(self, generated_password):
        """
        Changes the domain name.
        """
        if generated_password:
            answer = input("Changing the domain names entails a change of the "
                + "generated password. Are you sure you want to change the " +
                "  domain name? [y/n] ")
            if answer in ["n", "N", "no", "No", "NO", "not", "Not", "NOT",
                "nay", "Nay", "NAY", "nein", "Nein", "NEIN"]:
                return
        print("Current domain name: " + self.get_domain())
        self.set_domain(input("New domain name: "))
        while len(self.get_domain()) < 1:
            print("The new domain name must consist of at least one character.")
            self.set_domain(input("New domain name: "))
        input("The domain name was changed. Press any key to continue.")

    def has_username(self):
        """
        Returns True if the username is set.

        :return: username set?
        :rtype: bool
        """
        return self.username and len(str(self.username)) > 0

    def get_username(self):
        """
        Returns the username or an empty string if it is not set.

        :return: the username
        :rtype: str
        """
        if self.username:
            return self.username
        else:
            return ""

    def set_username(self, username):
        """
        Sets the username.

        :param username: a username
        :type username: str
        """
        self.username = username

    def change_delete_username(self):
        """
        Changes or deletes the username.
        """
        if self.has_username():
            print("Current username: " + self.get_username())
            self.set_username(input("Enter a new username or press Enter " +
                "to delete the username: "))
            while len(self.get_username()) < 1:
                answer = input("Are you sure you want to delete the username? "
                    + "[y/n] ")
                if answer not in ["n", "N", "no", "No", "NO", "not", "Not",
                    "NOT", "nay", "Nay", "NAY", "nein", "Nein", "NEIN"]:
                    self.set_username("")
                    break
                else:
                    self.set_username(input("Enter a new username or press " +
                        "Enter to delete the username: "))
            if len(self.get_username()) < 1:
                input("The username was deleted. Press any key to continue.")
            else:
                input("The username was changed. Press any key to continue.")
        else:
            self.set_username(input("Enter a username or press Enter to " +
                "abort: "))
            if len(self.get_username()) < 1:
                input("No username was set. Press any key to continue.")
            else:
                input("The username was set. Press any key to continue.")

    def has_fixed_password(self):
        """
        Returns True if the fixed password is set.

        :return: fixed password set?
        :rtype: bool
        """
        return self.fixed_password and len(str(self.fixed_password)) > 0

    def get_fixed_password(self):
        """
        Returns the fixed password or an empty string if it is not set.

        :return: the fixed password
        :rtype: str
        """
        if self.fixed_password:
            return self.fixed_password
        else:
            return ""

    def set_fixed_password(self, fixed_password):
        """
        Sets the fixed password.

        :param fixed_password: a fixed password
        :type fixed_password: str
        """
        self.fixed_password = fixed_password

    @staticmethod
    def get_default_character_set():
        """
        Returns the default character set.

        :return: the default character set
        :rtype: str
        """
        return DEFAULT_DIGITS + DEFAULT_LOWER_CASE_CHARACTERS + \
            DEFAULT_UPPER_CASE_CHARACTERS + DEFAULT_EXTRA_CHARACTERS

    @staticmethod
    def get_lower_case_character_set():
        """
        Returns the lower case character set.

        :return: the lower case character set
        :rtype: str
        """
        return DEFAULT_LOWER_CASE_CHARACTERS

    @staticmethod
    def get_upper_case_character_set():
        """
        Returns the upper case character set.

        :return: the upper case character set
        :rtype: str
        """
        return DEFAULT_UPPER_CASE_CHARACTERS

    @staticmethod
    def get_digits_character_set():
        """
        Returns the digit character set.

        :return: the digit character set
        :rtype: str
        """
        return DEFAULT_DIGITS

    def get_character_set(self):
        """
        Returns the whole character set.

        :return: the whole character set
        :rtype: str
        """
        used_characters = ""
        if "n" in self.get_template():
            used_characters += DEFAULT_DIGITS
        if "a" in self.get_template():
            used_characters += DEFAULT_LOWER_CASE_CHARACTERS
        if "A" in self.get_template():
            used_characters += DEFAULT_UPPER_CASE_CHARACTERS
        if "o" in self.get_template():
            used_characters += self.get_extra_character_set()
        return used_characters

    def get_extra_character_set(self):
        """
        Returns the special character set.

        :return: the special characters set
        :rtype: str
        """
        return self.extra_characters

    def set_extra_character_set(self, extra_set):
        """
        Sets the extra character set.

        :param extra_set: the extra character set
        :type extra_set: str
        """
        if extra_set is None or len(extra_set) <= 0:
            self.extra_characters = DEFAULT_EXTRA_CHARACTERS
        else:
            self.extra_characters = extra_set

    def get_salt(self):
        """
        Returns the salt.

        :return: the salt
        :rtype: bytes
        """
        return self.salt

    def set_salt(self, salt):
        """
        Sets the salt. Normally bytes should be passed as the salt. For
        convenience this method also accepts strings which are UTF-8 encoded
        and stored in binary format.

        :param salt: a salt
        :type salt: bytes or str
        """
        if type(salt) == bytes:
            self.salt = salt
        elif type(salt) == str:
            self.salt = salt.encode("utf-8")
        else:
            raise TypeError("The passed salt should be of type byte or string.")

    def new_salt(self):
        """
        Creates a new salt for the setting.
        """
        self.salt = Crypter.create_salt()

    def get_length(self):
        """
        Returns the password length.

        :return: the password length
        :rtype: int
        """
        return self.length

    def set_length(self, length):
        """
        Sets the password length.
        
        :param iterations: a password length
        :type iterations: int
        """
        self.length = length
        self.set_complexity(self.get_complexity())

    def get_iterations(self):
        """
        Returns the iteration count.

        :return: the iteration count
        :rtype: int
        """
        return self.iterations

    def set_iterations(self, iterations):
        """
        Sets the iteration count.

        :param iterations: an iteration count
        :type iterations: int
        """
        self.iterations = iterations

    def get_c_date(self):
        """
        Returns the creation date as a datetime object.

        :return: the creation date
        :rtype: datetime
        """
        return self.creation_date

    def get_creation_date(self):
        """
        Returns the creation date as a string.

        :return: the creation date
        :rtype: str
        """
        return self.creation_date.strftime("%Y-%m-%dT%H:%M:%S")

    def set_creation_date(self, creation_date):
        """
        Sets the creation date.

        :param creation_date: a creation date
        :type creation_date: str
        """
        try:
            self.creation_date = datetime.strptime(creation_date,
                "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            print("This creation date has a wrong format: " + creation_date)
        if self.modification_date < self.creation_date:
            self.modification_date = self.creation_date

    def get_m_date(self):
        """
        Returns the modification date as a datetime object.

        :return: the modification date
        :rtype: datetime
        """
        return self.modification_date

    def get_modification_date(self):
        """
        Returns the modification date as string.

        :return: the modification date
        :rtype: str
        """
        return self.modification_date.strftime("%Y-%m-%dT%H:%M:%S")

    def set_modification_date(self, modification_date = None):
        """
        Sets the modification date.

        :param modification_date: a modification date
        :type modification_date: str
        """
        if type(modification_date) == str:
            try:
                self.modification_date = datetime.strptime(modification_date,
                    "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                print("This modification date has a wrong format: " +
                    modification_date)
        else:
            self.modification_date = datetime.now()
        if self.modification_date < self.creation_date:
            self.creation_date = self.modification_date

    def get_notes(self):
        """
        Returns the notes or an empty string if they are not set.

        :return: the notes
        :rtype: str
        """
        if self.notes:
            return self.notes
        else:
            return ""

    def set_notes(self, notes):
        """
        Sets the notes.

        :param notes: notes
        :type notes: str
        """
        self.notes = notes
    
    def change_delete_notes(self):
        """
        Changes or deletes the notes.
        """
        if self.get_notes():
            print("Current notes: " + self.get_notes())
            self.set_notes(input("Enter new notes or press Enter to delete the "
                + "notes: "))
            while len(self.get_notes()) < 1:
                answer = input("Are you sure you want to delete the notes? " +
                    "[y/n] ")
                if answer not in ["n", "N", "no", "No", "NO", "not", "Not",
                    "NOT", "nay", "Nay", "NAY", "nein", "Nein", "NEIN"]:
                    self.set_notes("")
                    break
                else:
                    self.set_notes(input("Enter new notes or press Enter to " +
                        "delete the notes: "))
            if len(self.get_notes()) < 1:
                input("The notes were deleted. Press any key to continue.")
            else:
                input("The notes were changed. Press any key to continue.")
        else:
            self.set_notes(input("Enter notes or press Enter to abort: "))
            if len(self.get_notes()) < 1:
                input("No notes were set. Press any key to continue.")
            else:
                input("The notes were set. Press any key to continue.")

    def get_url(self):
        """
        Returns the url or an empty string if it is not set.

        :return: the url
        :rtype: str
        """
        if self.url:
            return self.url
        else:
            return ""

    def set_url(self, url):
        """
        Sets the url.

        :param url: an url
        :type url: str
        """
        self.url = url

    def change_delete_url(self):
        """
        Changes or deletes the URL.
        """
        if self.get_url():
            print("Current URL: " + self.get_url())
            self.set_url(input("Enter a new URL or press Enter to delete the "
                + "URL: "))
            while len(self.get_url()) < 1:
                answer = input("Are you sure you want to delete the URL? [y/n] ")
                if answer not in ["n", "N", "no", "No", "NO", "not", "Not",
                    "NOT", "nay", "Nay", "NAY", "nein", "Nein", "NEIN"]:
                    self.set_url("")
                    break
                else:
                    self.set_url(input("Enter a new URL or press Enter to " +
                        "delete the URL: "))
            if len(self.get_url()) < 1:
                input("The URL was deleted. Press any key to continue.")
            else:
                input("The URL was changed. Press any key to continue.")
        else:
            self.set_url(input("Enter a URL or press Enter to abort: "))
            if len(self.get_url()) < 1:
                input("No URL was set. Press any key to continue.")
            else:
                input("The URL was set. Press any key to continue.")

    def calculate_template(self, use_lower_case = None, use_upper_case = None,
        use_digits = None, use_extra = None):
        """
        Calculates a new template based on the character set and the password
        length.

        :param use_extra: Use extra characters? Gets this setting from the
            current template if set to None.
        :type use_extra: bool
        :param use_digits: Use digits? Gets this setting from the current
            template if set to None.
        :type use_digits: bool
        :param use_upper_case: Use upper case characters? Gets this setting
            from the current template if set to None.
        :type use_upper_case: bool
        :param use_lower_case: Use lower case characters? Gets this setting
            from the current template if set to None.
        :type use_lower_case: bool
        """
        if use_lower_case is None:
            use_lower_case = "a" in self.get_template()
        if use_upper_case is None:
            use_upper_case = "A" in self.get_template()
        if use_digits is None:
            use_digits = "n" in self.get_template()
        if use_extra is None:
            use_extra = "o" in self.get_template()
        len = []
        inserted_lower = False
        inserted_upper = False
        inserted_digit = False
        inserted_extra = False
        for i in range(self.get_length()):
            if use_lower_case and not inserted_lower:
                len.append("a")
                inserted_lower = True
            elif use_upper_case and not inserted_upper:
                len.append("A")
                inserted_upper = True
            elif use_digits and not inserted_digit:
                len.append("n")
                inserted_digit = True
            elif use_extra and not inserted_extra:
                len.append("o")
                inserted_extra = True
            else:
                len.append("x")
        shuffle(len)
        self.template = "".join(len)

    def get_template(self):
        """
        Returns the template.

        :return: the template
        :rtype: str
        """
        return self.template

    def set_complexity(self, complexity):
        """
        Sets the complexity.
        1: digits
        2: lower case characters
        3: upper case characters
        4: digits and lower case characters
        5: digits and upper case characters
        6: digits, lower case characters, and upper case characters
        7: digits, lower case characters, upper case characters, and extra
        characters
        8: extra characters

        :param complexity: a digit from 1 to 8
        :type complexity: int
        """
        if not 1 <= complexity <= 8:
            ValueError("The complexity must be an integer in the range 1 to 8.")
        if complexity == 1:
            self.calculate_template(False, False, True, False)
        elif complexity == 2:
            self.calculate_template(True, False, False, False)
        elif complexity == 3:
            self.calculate_template(False, True, False, False)
        elif complexity == 4:
            self.calculate_template(True, False, True, False)
        elif complexity == 5:
            self.calculate_template(False, True, True, False)
        elif complexity == 6:
            self.calculate_template(True, True, True, False)
        elif complexity == 7:
            self.calculate_template(True, True, True, True)
        elif complexity == 8:
            self.calculate_template(False, False, False, True)

    def get_complexity(self):
        """
        Returns the complexity. If the character selection does not match -1 is
        returned.

        :return: a digit from 1 to 8 or -1
        :rtype: int
        """
        if "n" in self.get_template() and "a" not in self.get_template() and \
            "A" not in self.get_template() and "o" not in self.get_template():
            return 1
        elif "n" not in self.get_template() and "a" in self.get_template() and \
            "A" not in self.get_template() and "o" not in self.get_template():
            return 2
        elif "n" not in self.get_template() and "a" not in self.get_template() \
            and "A" in self.get_template() and "o" not in self.get_template():
            return 3
        elif "n" in self.get_template() and "a" in self.get_template() and \
            "A" not in self.get_template() and "o" not in self.get_template():
            return 4
        elif "n" not in self.get_template() and "a" in self.get_template() and \
            "A" in self.get_template() and "o" not in self.get_template():
            return 5
        elif "n" in self.get_template() and "a" in self.get_template() and \
            "A" in self.get_template() and "o" not in self.get_template():
            return 6
        elif "n" in self.get_template() and "a" in self.get_template() and \
            "A" in self.get_template() and "o" in self.get_template():
            return 7
        elif "n" not in self.get_template() and "a" not in self.get_template() \
            and "A" not in self.get_template() and "o" in self.get_template():
            return 8
        else:
            return -1

    def to_dict(self):
        """
        Returns a dictionary with the settings.

        :return: the settings dictionary
        :rtype: dict
        """
        domain_object = {"domain name": self.get_domain()}
        if self.get_username():
            domain_object["username"] = self.get_username()
        if self.get_fixed_password():
            domain_object["fixed_password"] = self.get_fixed_password()
        domain_object["length"] = self.get_length()
        domain_object["extra_character_set"] = self.get_extra_character_set()
        domain_object["iterations"] = self.get_iterations()
        domain_object["salt"] = str(b64encode(self.get_salt()),
            encoding = "utf-8")
        domain_object["template"] = self.get_template()
        if self.get_url():
            domain_object["URL"] = self.get_url()
        if self.notes:
            domain_object["notes"] = self.get_notes()
        domain_object["creation_date"] = self.get_creation_date()
        domain_object["modification_date"] = self.get_modification_date()
        return domain_object

    def load_from_dict(self, loaded_setting):
        """
        Loads the settings from a dictionary.

        :param loaded_setting: a settings dictionary
        :type loaded_setting: dict
        """
        if "username" in loaded_setting:
            self.set_username(loaded_setting["username"])
        if "fixed_password" in loaded_setting:
            self.set_fixed_password(loaded_setting["fixed_password"])
        if "length" in loaded_setting:
            self.set_length(loaded_setting["length"])
        if "extra_character_set" in loaded_setting:
            self.set_extra_character_set(loaded_setting["extra_character_set"])
        if "iterations" in loaded_setting:
            self.set_iterations(loaded_setting["iterations"])
        if "salt" in loaded_setting:
            self.set_salt(b64decode(loaded_setting["salt"]))
        if "template" in loaded_setting:
            self.template = loaded_setting["template"]
        if "URL" in loaded_setting:
            self.set_url(loaded_setting["URL"])
        if "notes" in loaded_setting:
            self.set_notes(loaded_setting["notes"])
        if "creation_date" in loaded_setting:
            self.set_creation_date(loaded_setting["creation_date"])
        if "modification_date" in loaded_setting:
            self.set_modification_date(loaded_setting["modification_date"])

    def set_generated_password(self):
        """
        Displays input prompts for the settings pertaining to a generated
        password.
        """
        length_str = input("Password length: ")
        while True:
            try:
                length_int = int(length_str)
                if length_int <= 0:
                    print("The password length must be greater than 0.")
                    length_str = input("New password length: ")
                else:
                    self.set_length(length_int)
                    break
            except ValueError:
                print("The password length must be an integer.")
                length_str = input("New password length: ")
        option = input("Choose a password complexity:\n1\tdigits\n2\tlower " +
            "case characters" + "\n3\tupper case characters\n4\tdigits and " +
            "lower case characters" + "\n5\tdigits and upper case characters" +
            "\n6\tdigits, lower case characters, and upper case characters\n7" +
            "\tdigits, lower case characters, upper case characters, and extra "
            + "characters\n8\textra characters\n[1/2/3/4/5/6/7/8] ")
        while option not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            option = input('Enter "1", "2", "3", "4", "5", "6", "7", or "8": ')
        self.set_complexity(int(option))
        if option in ["7", "8"]:
            print("Extra character set: " + self.get_extra_character_set())
            answer = input("Change extra character set? [y/n] ")
            if answer not in ["n", "N", "no", "No", "NO", "not", "Not", "NOT",
                "nay", "Nay", "NAY", "nein", "Nein", "NEIN"]:
                self.set_extra_character_set(input("New extra character set: "))
        print("Password generation was successful.")

    def new_domain(self):
        """
        Displays input prompts for the username and the password for a new
        domain.
        """
        answer = input("Set a username? [y/n] ")
        if answer not in ["n", "N", "no", "No", "NO", "not", "Not", "NOT",
            "nay", "Nay", "NAY", "nein", "Nein", "NEIN"]:
            self.set_username(input("Username: "))
            while len(self.get_username()) < 1:
                print("The username must consist of at least one character.")
                self.set_username(input("Username: "))
        answer = input("Generate a password (alternatively a fixed password " +
            "can be stored)? [y/n] ")
        if answer in ["n", "N", "no", "No", "NO", "not", "Not", "NOT", "nay",
            "Nay", "NAY", "nein", "Nein", "NEIN"]:
            self.set_fixed_password(getpass.getpass("Fixed password: "))
            while len(self.get_fixed_password()) < 1:
                print("The fixed password must consist of at least one " +
                    "character.")
                self.set_fixed_password(getpass.getpass("Fixed password: "))
        else:
            self.set_generated_password()

    def get_settings(self):
        """
        Displays settings.
        """
        print("Domain name: " + self.get_domain())
        if self.has_username():
            print("Username: " + self.get_username())
        if not self.has_fixed_password():
            print("Password length: " + str(self.get_length()))
            if self.get_complexity() == 1:
                print("Password complexity: digits")
            elif self.get_complexity() == 2:
                print("Password complexity: lower case characters")
            elif self.get_complexity() == 3:
                print("Password complexity: upper case characters")
            elif self.get_complexity() == 4:
                print("Password complexity: digits and lower case characters")
            elif self.get_complexity() == 5:
                print("Password complexity: digits and upper case characters")
            elif self.get_complexity() == 6:
                print("Password complexity: digits, lower case characters, and "
                    + "upper case characters")
            elif self.get_complexity() == 7:
                print("Password complexity: digits, lower case characters, " +
                    "upper case characters, and extra characters")
                print("Extra character set: " + self.get_extra_character_set())
            else:
                print("Password complexity: extra characters")
                print("Extra character set: " + self.get_extra_character_set())
        if self.get_url() != "":
            print("URL: " + self.get_url())
        if self.get_notes() != "":
            print("Notes: " + self.get_notes())
        print("Creation date: " + self.get_creation_date())
        print("Modification date: " + self.get_modification_date())
        input("Press any key to continue.")

    def set_settings_menu_generated_password(self):
        """
        Menu to change and delete settings. Is called if the password was
        generated.
        """
        while True:
            print("Choose one of the following options:\n1\tchange domain name")
            if self.has_username():
                print("2\tchange or delete username")
            else:
                print("2\tset username")
            print("3\tset fixed password (the generated password will be " +
                "deleted)")
            print("4\tchange password length")
            print("5\tchange password complexity")
            if self.get_url():
                print("6\tchange or delete URL")
            else:
                print("6\tset URL")
            if self.get_notes():
                print("7\tchange or delete notes")
            else:
                print("7\tset notes")
            option = input("8\treturn to previous menu\n[1/2/3/4/5/6/7/8] ")
            while option not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                option = input('Enter "1", "2", "3", "4", "5", "6", "7", or ' +
                    '"8": ')
            if option == "1":
                self.change_domain(generated_password = True)
            elif option == "2":
                self.change_delete_username()
            elif option == "3":
                answer = input("Are you sure you want to delete the generated "
                    + "password [y/n] ")
                if answer not in ["n", "N", "no", "No", "NO", "not", "Not",
                    "NOT", "nay", "Nay", "NAY", "nein", "Nein", "NEIN"]:
                    self.set_fixed_password(getpass.getpass("Fixed password: "))
                    while len(self.get_fixed_password()) < 1:
                        print("The fixed password must consist of at least one "
                            + "character.")
                        self.set_fixed_password(getpass.getpass("Fixed " +
                            "password: "))
                    input("The generated password was deleted and the fixed " +
                        "password was set. Press any key to continue.")
                    self.set_settings_menu_fixed_password()
                    break
            elif option == "4":
                print("Current password length: " + str(self.get_length()))
                length_str = input("New password length: ")
                while True:
                    try:
                        length = int(length_str)
                        if length <= 0:
                            print("The password length must be greater than 0.")
                            length_str = input("New password length: ")
                        else:
                            self.set_length(length)
                            break
                    except ValueError:
                        print("The password length must be an integer.")
                        length_str = input("New password length: ")
                input("The password length was changed. Press any key to " +
                    "continue.")
            elif option == "5":
                if self.get_complexity() == 1:
                    print("Current password complexity: digits")
                elif self.get_complexity() == 2:
                    print("Current password complexity: lower case characters")
                elif self.get_complexity() == 3:
                    print("Current password complexity: upper case characters")
                elif self.get_complexity() == 4:
                    print("Current password complexity: digits and lower case "
                        + "characters")
                elif self.get_complexity() == 5:
                    print("Current password complexity: digits and upper case "
                        + "characters")
                elif self.get_complexity() == 6:
                    print("Current password complexity: digits, lower case "
                        + "characters, and upper case characters")
                elif self.get_complexity() == 7:
                    print("Current password complexity: digits, lower case " +
                        "characters, upper case characters, and extra " +
                        "characters")
                else:
                    print("Current password complexity: extra characters")
                option_complexity = input("Choose a new password complexity:" +
                    "\n1\tdigits\n2\tlower case characters\n3\tupper case " +
                    "characters\n4\tdigits and lower case characters\n5\t" +
                    "digits and upper case characters\n6\tdigits, lower case " +
                    "characters, and upper case characters\n7\tdigits, lower " +
                    "case characters, upper case characters, and extra " +
                    "characters\n8\textra characters\n[1/2/3/4/5/6/7/8] ")
                while option_complexity not in ["1", "2", "3", "4", "5", "6",
                    "7", "8"]:
                    option_complexity = input('Enter "1", "2", "3", "4", "5", '
                        + '"6", "7", or "8": ')
                self.set_complexity(int(option_complexity))
                if option_complexity in ["7", "8"]:
                    print("Current extra character set: " +
                        self.get_extra_character_set())
                    answer = input("Change extra character set? [y/n] ")
                    if answer not in ["n", "N", "no", "No", "NO", "not", "Not",
                        "NOT", "nay", "Nay", "NAY", "nein", "Nein", "NEIN"]:
                        self.set_extra_character_set(input("New extra " +
                            "character set: "))
                input("The password complexity was changed. Press any key to " +
                    "continue.")
            elif option == "6":
                self.change_delete_url()
            elif option == "7":
                self.change_delete_notes()
            else:
                break

    def set_settings_menu_fixed_password(self):
        """
        Menu to change and delete settings. Is called if a fixed password was
        set.
        """
        while True:
            print("Choose one of the following options:\n1\tchange domain name")
            if self.has_username():
                print("2\tchange or delete username")
            else:
                print("2\tset username")
            print("3\tchange fixed password")
            print("4\tdelete fixed password (a password will be generated)")
            if self.get_url():
                print("5\tchange or delete URL")
            else:
                print("5\tset URL")
            if self.get_notes():
                print("6\tchange or delete notes")
            else:
                print("6\tset notes")
            option = input("7\treturn to previous menu\n[1/2/3/4/5/6/7] ")
            while option not in ["1", "2", "3", "4", "5", "6", "7"]:
                option = input('Enter "1", "2", "3", "4", "5", "6", or "7": ')
            if option == "1":
                self.change_domain(generated_password = False)
            elif option == "2":
                self.change_delete_username()
            elif option == "3":
                print("Current fixed password: " + self.get_fixed_password())
                self.set_fixed_password(getpass.getpass("New fixed password: "))
                while len(self.get_fixed_password()) < 1:
                    print("The new fixed password must consist of at least one "
                        + "character.")
                    self.set_fixed_password(getpass.getpass("New fixed " +
                        "password: "))
                input("The fixed password was changed. Press any key to " +
                    "continue.")
            elif option == "4":
                answer = input("Are you sure you want to delete the fixed " +
                    "password? [y/n] ")
                if answer not in ["n", "N", "no", "No", "NO", "not", "Not",
                    "NOT", "nay", "Nay", "NAY", "nein", "Nein", "NEIN"]:
                    self.set_fixed_password("")
                    self.set_generated_password()
                    input("The fixed password was deleted and a password was " +
                        "generated. Press any key to continue.")
                    self.set_settings_menu_generated_password()
                    break
            elif option == "5":
                self.change_delete_url()
            elif option == "6":
                self.change_delete_notes()
            else:
                break
