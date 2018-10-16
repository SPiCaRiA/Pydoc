#!/usr/bin/python
#-*- coding=utf-8 -*-

import sys


class LexError(Exception):
    def __init__(self, line_content, line):
        self.line_content = line_content
        self.line = line

    def warning(self, filename):
        from localestring import warning
        sys.stderr.write(warning("syntax_error") % (filename, self.line))
        sys.stderr.write(self.line_content + "\n")
        sys.exit(1)


class FileNotFoundError(Exception):
    def __init__(self, filename):
        self.filename = filename

    def write_error(self):
        from localestring import warning
        sys.stderr.write(warning("file_not_exist") + "\n")


class InvalidStringError(Exception):
    def __init__(self, string_type):
        self.string_type = "Error: invalid %s\n" % string_type

    def write_error(self):
        sys.stderr.write(self.string_type)


class ParseError(Exception):
    def __init__(self):
        pass

    @staticmethod
    def write_error():
        from localestring import warning
        sys.stderr.write(warning("parse_error") + "\n")


class GenerateError(Exception):
    def __init__(self):
        pass

    @staticmethod
    def write_error():
        from localestring import warning
        sys.stderr.write(warning("generate_error") + "\n")

class FileTypeError(Exception):
    def __init__(self, filename):
        self.filename = filename

    @staticmethod
    def write_error():
        from localestring import warning
        sys.stderr.write(warning("wrong_file_type") + "\n")
