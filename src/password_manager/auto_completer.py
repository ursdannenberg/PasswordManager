#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
AutoCompleter handles autocompletion based on the list of domain names.
"""

class AutoCompleter(object):
    
    def __init__(self, options):
        self.options = sorted(options)
    
    def complete(self, text, state):
        if state == 0:
            if text:
                self.matches = [option for option in self.options if option and
                    option.startswith(text)]
            else:
                self.matches = self.options[:]
        try:
            return self.matches[state]
        except IndexError:
            return None
