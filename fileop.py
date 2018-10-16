#!/usr/bin/python
#-*- coding=utf-8 -*-

import os.path
import sys
import shutil

from excepts import FileNotFoundError, LexError, FileTypeError
from localestring import warning
from lexer import Lexer
from Generator import Generator


class FileOp():
    def __init__(self, filename, output):
        self.filename = os.path.expanduser(filename).replace("\\", "/")
        self.mode = os.path.isdir(self.filename) and "dir" or "single"
        self.output = os.path.expanduser(output).replace("\\", "/")

    def __call__(self):
        self.operation()

    """
    This method decide the way of processing input in dir mode or file mode
    @version 1.0
    @author Gabriel
    """
    def operation(self):
        if self.mode == "dir":
            self.dir_op()
        else:
            self.file_op()

    """
    This method create the html doc file for source code in single file mode
    @version 1.0
    @author Gabriel
    """
    def file_op(self):
        if self.filename.split(".")[-1] != "py":
            raise FileTypeError(self.filename)
        self.read_write(self.filename, self.open_file(self.parse_output([self.filename])[0]))
        if not os.path.isdir(self.output):
            self.output = self.output_dir()
        style_css = os.path.dirname(os.path.realpath(__file__)) + "/style.css"
        try:
            shutil.copyfile(style_css, os.path.join(self.output, "style.css"))
        except IOError:
            pass

    def output_dir(self):
        filename_len = len(self.output.split("/")[-1])
        return self.output[:len(self.output) - filename_len]

    """
    This method create the html doc files for the package in dir mode
    @version 1.0
    @author Gabriel
    """
    def dir_op(self):
        file_list = self.walk_dir(self.filename)
        filename_list = self.parse_file(file_list)
        output_list = self.parse_output(filename_list)

        for index in range(len(filename_list)):
            self.read_write(filename_list[index], self.open_file(output_list[index]))

        self.write_index(output_list)
        self.write_main(output_list)
        style_css = os.path.dirname(os.path.realpath(__file__)) + "/style.css"
        try:
            shutil.copyfile(style_css, os.path.join(self.output, "style.css"))
        except IOError:
            pass

    """
    This method walk through all the files in the directory and return them
    @version 1.0
    @author Gabriel
    @param base directory
    @return the file list under the base directory
    """
    def walk_dir(self, base):
        current_dir_list = []
        current_file_list = []

        root, dirs, files = os.walk(base).next()
        for file in files:
            current_file_list.append(os.path.join(root, file))

        if len(dirs) == 0:
            return [current_file_list, dirs, root]
        else:
            for directory in dirs:
                current_dir_list.append(self.walk_dir(os.path.join(root, directory)))
            return [current_file_list, current_dir_list, root]

    """
    This method parse the file list walk_dir() returns in one flat array
    @version 1.0
    @author Gabriel
    @param file list
    @return the one dimensional array parsed from file list
    """
    def parse_file(self, file_list):
        result = []
        for file in file_list[0]:
            if file.split(".")[-1] == "py":
                result.append(file)

        if len(file_list[1]) == 0:
            return result
        else:
            for directory in file_list[1]:
                result += self.parse_file(directory)

    """
    This method parse the output file list into valid file name list
    @version 1.0
    @author Gabriel
    @param file list
    @return list of processed valid file name
    """
    def parse_output(self, file_list):
        result = []
        file_parsed = self.expand_filename(file_list)

        for file_path in file_parsed:
            if not ".pyc" in file_path:
                result.append(os.path.join(self.output, "docs/", file_path) + ".html")
        return result

    """
    This method replace the "/" in file name to "." to make the file name valid
    @version 1.0
    @author Gabriel
    @param file list
    @return processed valid file name
    """
    @staticmethod
    def expand_filename(file_list):
        result = []
        for file_name in file_list:
            result.append(file_name.strip(".py").replace("/", ".").strip("."))
        return result

    """
    This method read the content from source code file and write the parsed comment into html doc file
    @version 1.0
    @author Gabriel
    @param source code file, output file
    """
    def read_write(self, file, output):
        source_content = self.read_file(file)
        try:
            self.write_file(output, Generator(Lexer(source_content)(), self.mode, "html", file)())
        except LexError, e:
            sys.stderr.write(warning("syntax_error") % (self.filename, e.line))
            sys.stderr.write(e.line_content + "\n")
            sys.exit(1)

    """
    This method create and write the content into index html doc file
    @version 1.0
    @author Gabriel
    @param file list
    """
    def write_index(self, file_list):
        self.write_file(self.open_file(os.path.join(self.output, "index.html")), Generator.generate_index("html",
                                                                                                          file_list))

    """
    This method create and write the content into main frame html doc file
    @version 1.0
    @author Gabriel
    @param file list
    """
    def write_main(self, file_list):
        self.write_file(self.open_file(os.path.join(self.output, "index_main.html")),
                        Generator.generate_main("html", file_list))

    """
    This method is used to read a file
    @version 1.0
    @author Gabriel
    @param file name to read
    @return the handle of the file
    """
    @staticmethod
    def read_file(file):
        if not os.path.exists(file):
            raise FileNotFoundError(file)
        with open(file, "r") as source_file:
            content = source_file.read()

        return content

    """
    This method is used to create a file
    @version 1.0
    @author Gabriel
    @param file name to create
    @return the handle of the file created
    """
    def open_file(self, output):
        if not os.path.exists(os.path.dirname(output)):
            os.makedirs(os.path.dirname(output))

        return open(output, "w")

    """
    This method is used to write content into a file
    @version 1.0
    @author Gabriel
    @param output file, content to write
    """
    def write_file(self, output, content):
        output.write(str(content))


"""
This function is used to test this module
@version 1.0
@author Gabriel
"""
def test():
    FileOp("~/test/fileop.py", "~/桌面/test_pydoc")()
    print "over"

if __name__ == "__main__":
    test()
