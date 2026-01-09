import argparse
import getpass
import readline
import sys

from password_manager.key_generation_key_manager import KeyGenerationKeyManager
from password_manager.password_manager import create_settings_manager, has_setting, get_password, setting_menu
from password_manager.auto_completer import AutoCompleter


def main() -> None:
    parser = argparse.ArgumentParser(description="Secure password manager " +
                                                 "for the Unix shell")
    parser.add_argument("-q", "--quiet", action="store_const", const=True,
                        help="Only prompts for master password and domain name and copies " +
                             "username and password to the clipboard.")
    args = parser.parse_args()
    master_password = getpass.getpass(prompt="Master password: ")
    key_generation_key_manager = KeyGenerationKeyManager()
    settings_manager, preference_manager = \
        create_settings_manager(key_generation_key_manager, master_password)
    # key_generation_key_exists = len(
    #     preference_manager.get_key_generation_key_block()) == 112
    try:
        settings_manager.load_settings(key_generation_key_manager)
    except PermissionError:
        print("Wrong master password.")
        sys.exit(1)
    while True:
        completer = AutoCompleter(settings_manager.get_domain_list())
        completer_delimiters = readline.get_completer_delims()
        completer_delimiters = completer_delimiters.translate(
            {ord(character): None for character in " @-"})
        readline.set_completer_delims(completer_delimiters)
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')
        domain = input("Enter a domain name or press Enter to quit: ")
        if domain == "":
            sys.exit(1)
        domain, setting_found = has_setting(domain)
        if args.quiet:
            if setting_found:
                setting = settings_manager.get_setting(domain)
                get_password(setting,
                             key_generation_key_manager.get_key_generation_key(),
                             option="1")
        else:
            if setting_found:
                setting = settings_manager.get_setting(domain)
                print('Loaded settings for "' + domain + '".')
                setting_menu(setting, key_generation_key_manager,
                             settings_manager)
            else:
                print('For "' + domain + '" no settings were found.')
                answer = input("Create a new domain? [y/n] ")
                if answer in ["n", "N", "no", "No", "NO", "not", "Not", "NOT",
                              "nay", "Nay", "NAY", "nein", "Nein", "NEIN"]:
                    input("No domain was created. Press any key to continue.")
                else:
                    setting = settings_manager.get_setting(domain)
                    setting.new_domain()
                    settings_manager.set_setting(setting)
                    settings_manager.store_settings(key_generation_key_manager)
                    input("The new domain was created. Press any key to " +
                          "continue.")
                    setting_menu(setting, key_generation_key_manager,
                                 settings_manager)

if __name__ == "__main__":
    main()