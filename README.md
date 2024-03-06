## PasswordManager
PasswordManager is a secure password manager for the Unix shell. PasswordManager is written in Python 3 and based on [Qt-SESAM](https://github.com/ola-ct/Qt-SESAM). Details on the security can be found in the section Internals in the [Qt-SESAM documentation](https://ola-ct.github.io/Qt-SESAM/index.en.html), with a few differences:
* PasswordManager uses only the domain name, not the username, for the password generation.
* No version flag is used.

Required Python modules:
* [pycrypto](https://www.dlitz.net/software/pycrypto/)
* [pyperclip](https://github.com/asweigart/pyperclip)
* [termcolor](https://github.com/termcolor/termcolor)
