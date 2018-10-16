#!/usr/bin/python
# -*- coding=utf-8 -*-

from doctype import doc_type
from HTMLMapParser import HTMLMapParser
from excepts import GenerateError
from MapGenerator import MapGenerator


class Generator():
    def __init__(self, map, file_mode, mode, filename):
        self.map = map
        self.mode = mode
        self.file_mode = file_mode
        self.filename = filename

    def __call__(self):
        return self.generate_file()

    """
    This method will generate the html doc string for the file
    @version 1.0
    @author Benny
    @return the html doc string
    """

    def generate_file(self):
        if self.mode in doc_type:
            try:
                result = doc_type[self.mode](HTMLMapParser(MapGenerator(self.map)(), self.filename)(), self.filename)()
            except GenerateError, e:
                e.write_error()
            return result

    """
    This method will generate the html doc string for the index file
    @version 1.0
    @author Benny
    @param type of doc file format, file list
    @return the html doc string for the index file
    """

    @classmethod
    def generate_index(cls, mode, file_list):
        if mode in doc_type:
            try:
                result = doc_type[mode].generate_index(file_list)
            except GenerateError, e:
                e.write_error()
            return result

    """
    This method will generate the html doc string for the main frame
    @version 1.0
    @author Benny
    @param type of doc file format, file list
    @return the html doc string for the index file
    """

    @classmethod
    def generate_main(cls, mode, file_list):
        if mode in doc_type:
            try:
                result = doc_type[mode].generate_main(file_list)
            except GenerateError, e:
                e.write_error()
            return result
