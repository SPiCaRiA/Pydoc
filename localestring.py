#!/usr/bin/python
#-*- coding=utf-8 -*-

import locale

from lang import *
from excepts import InvalidStringError

current_district = locale.getdefaultlocale()[0].lower()


"""
This function get the warning string from the lang_dict
@version 1.0
@author Joe
@param warning type
@return the warning string
"""
def warning(warn_type):
    if warn_type in warning_dict:
        warn = warning_dict[warn_type]
    else:
        raise InvalidStringError("warning")

    if current_district in warn:
        return warn[current_district]
    else:
        return warn["en_us"]


"""
This function get the string used in doc from the lang_dict
@version 1.0
@author Joe
@param doc string to use
@return the doc string needed
"""
def get_doc_string(doc_string):
    if doc_string in doc_dict:
        doc_string_dict = doc_dict[doc_string]
    else:
        raise InvalidStringError("doc string")

    if current_district in doc_string_dict:
        return doc_string_dict[current_district]
    else:
        return doc_string_dict["en_us"]


"""
This function get the help string used in menu
@version 1.0
@author Joe
@param help string to use
@return the help stirng
"""
def get_help_string(help_string):
    if help_string in help_dict:
        help_string_dict = help_dict[help_string]
    else:
        raise InvalidStringError("help string")

    if current_district in help_string_dict:
        return help_string_dict[current_district]
    else:
        return help_string_dict["en_us"]
