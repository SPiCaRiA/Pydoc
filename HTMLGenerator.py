#!/usr/bin/python
#-*- coding=utf-8 -*-

from templates import *
from string import Template
from localestring import get_doc_string
from excepts import GenerateError, InvalidStringError


class HTMLGenerator():
    COMMENT_MAP = {
        "_throws": get_doc_string("_throws"),
        "_return": get_doc_string("_return"),
        "_param": get_doc_string("_param"),
        "_author": get_doc_string("_author"),
        "_version": get_doc_string("_version"),
        "_since": get_doc_string("_since"),
    }

    def __init__(self, map, filename):
        self.map = map
        self.filename = filename

    def __call__(self):
        result = self.file_detail_string(self.map)
        if not result:
            raise GenerateError
        return result

    """
    This method generate the html doc string for the entire file
    @version 1.0
    @author Benny
    @param the file's infomation hash map
    @return the html doc string for the entire file
    """
    def file_detail_string(self, file):
        num_class = self.counter("class", file)
        substitute_map = {
            "filename": self.filename,
            "_file_annotation": get_doc_string("_file_annotation"),
        }
        substitute_map.update(file)
        template_string = file_detail_general % self.generate_doc_template("", file)
        substitute_map["class"] = ""

        for index in range(num_class):
            substitute_map["class"] += self.file_detail_class_string(file["class" + str(index + 1)])

        if not "file_doc_text" in file:
            substitute_map["file_doc_text"] = ""

        substitute_map["function_general"] = self.file_detail_function_general_string(file["function_general"])
        substitute_map["function_details"] = self.file_detail_function_details_string(file["function_details"])
        substitute_map.update(self.COMMENT_MAP)

        template = Template(template_string)
        return template.substitute(substitute_map)

    """
    This method generate the html doc string for an entire class.
    @version 1.0
    @author Benny
    @return the doc string of an entire class
    @param the hash map of the class' infomation
    """
    def file_detail_class_string(self, clazz):
        substitute_map = {
            "_class": get_doc_string("_class"),
            "class_name": clazz["class_name"],
            "super": self.file_detail_class_super_string(clazz),
            "class_comment": self.generate_class_doc_string(clazz["class_comment"]),
            "method_general": self.file_detail_class_method_general_string(clazz),
            "cons_general": self.file_detail_class_cons_general_string(clazz),
            "cons_details": self.file_detail_class_cons_details_string(clazz),
            "method_details": self.file_detail_class_method_details_string(clazz),
        }
        template = Template(file_detail_class)
        return template.substitute(substitute_map)

    """
    This method generate the html doc string for the super class
    @version 1.0
    @author Benny
    @return the doc string of the super class
    @param the hash map of class' infomation
    """
    def file_detail_class_super_string(self, clazz):
        template_string = self.file_detail_class_super_template(clazz)
        substitute_map = {}
        if not "super" in clazz:
            clazz["super"] = "object"

        if clazz["super"]:
            for key, super in clazz["super"].iteritems():
                substitute_map[key] = super
        template = Template(template_string)
        return template.substitute(substitute_map)

    """
    This method generate the template for the super classes of an class
    @version 1.0
    @author Benny
    @param the hash map of class' infomation
    @return the template for the super classes of an class
    """
    def file_detail_class_super_template(self, clazz):
        template = Template(file_detail_class_super)
        num_super = self.counter("super", clazz["super"])
        iter_string = ""

        for index in range(num_super):
            iter_string += file_detail_class_super_iter % (index + 1)

        return file_detail_class_super % iter_string

    """
    This method generate the html doc string for the methods' general infomation.
    @version 1.0
    @author Benny
    @return the doc string of the methods' general infomation
    @param the hash map of class' infomation
    """
    def file_detail_class_method_general_string(self, clazz):
        template_string = self.file_detail_class_method_general_template(clazz)
        substitute_map = {
            "_method_general": get_doc_string("_method_general"),
            "_method_general_table": get_doc_string("_method_general_table"),
            "_method": get_doc_string("_method"),
            "_param": get_doc_string("_param"),
        }
        template = Template(template_string)
        return template.substitute(substitute_map)

    """
    This method generate the template for the class' methods signature
    @version 1.0
    @author Benny
    @param the hash map of class' infomation
    @return the template of the class' methods
    """
    def file_detail_class_method_general_template(self, clazz):
        if not clazz:
            return ""
        num_method = self.count_procedure("method", clazz["method_general"])
        iter_string = ""
        substitute_map = {}
        substitute_map.update(clazz["method_general"])
        for index in range(num_method):
            substitute_map["method%d_args" % (index + 1)] = self.generate_procedure_args_template("method%d"
                                                                                                  % (index + 1),
                                                                                          clazz["method_general"])

        for index in range(num_method):
            iter_template = Template(file_detail_class_method_general_iter % (index % 2 and "altColor" or "rowColor",
                                                                              index + 1, index + 1))
            iter_string += iter_template.substitute(substitute_map)

        return file_detail_class_method_general % iter_string

    """
    This method generate the html doc string for the constructor's general infomation.
    @version 1.0
    @author Benny
    @return the doc string of the constructor's general infomation
    @param the hash map of class' infomation
    """
    def file_detail_class_cons_general_string(self, clazz):
        template_string = self.file_detail_class_cons_general_template(clazz)
        template = Template(template_string)
        substitute_map = {
            "_cons": get_doc_string("_cons"),
            "_cons_general": get_doc_string("_cons_general"),
            "_cons_general_table": get_doc_string("_cons_general_table"),
            "cons_args": self.generate_procedure_args_template("cons", clazz["cons_general"])
        }
        substitute_map.update(clazz["cons_general"])

        return template.substitute(substitute_map)

    """
    This method generate the template for the constructor's signature
    @version 1.0
    @author Benny
    @param the hash map of class' infomation
    @return the template for the constructor's signature
    """
    def file_detail_class_cons_general_template(self, clazz):
        return file_detail_class_cons_general

    """
    This method generate the html string for the constructor's detailed infomation.
    @version 1.0
    @author Benny
    @return the doc string of constructor's detailed infomation
    @param the hash map of class' infomation
    """
    def file_detail_class_cons_details_string(self, clazz):
        template_string = self.file_detail_class_cons_details_template(clazz)
        substitute_map = {
            "_cons_details": get_doc_string("_cons_details"),
            "cons_args": self.generate_procedure_args_template("cons", clazz["cons_details"])
        }
        substitute_map.update(clazz["cons_details"])
        substitute_map.update(self.COMMENT_MAP)

        if not "cons_doc_text" in substitute_map:
            substitute_map["cons_doc_text"] = ""

        template = Template(template_string)
        return template.substitute(substitute_map)

    def file_detail_class_cons_details_template(self, clazz):
        return file_detail_class_cons_details % self.generate_doc_template("", clazz["cons_details"])

    """
    This method generate the html doc string for the class' methods.
    @version 1.0
    @author Benny
    @return the html doc string for the class' methods' comment
    @param the hash map of the class' infomation
    """
    def file_detail_class_method_details_string(self, clazz):
        num_methods = self.count_procedure("method", clazz["method_details"])
        template_string = self.file_detail_class_method_details_template(clazz)
        substitute_map = {
            "_method_details": get_doc_string("_method_details"),
        }
        for index in range(num_methods):
            substitute_map["method" + str(index + 1) + "_doc_text"] = ""
        substitute_map.update(clazz["method_details"])
        substitute_map.update(self.COMMENT_MAP)

        for index in range(num_methods):
            substitute_map["method%d_args" % (index + 1)] = self.generate_procedure_args_template("method" +
                                                                                                  str(index + 1),
                                                                                              clazz["method_details"])

        template = Template(template_string)
        return template.substitute(substitute_map)

    def file_detail_class_method_details_template(self, clazz):
        num_methods = self.count_procedure("method", clazz["method_details"])
        iter_string = ""

        for index in range(num_methods):
            index += 1
            iter_string += file_detail_class_method_details_iter % (index, index, index, index,
                                                                    self.generate_doc_template("method%d" % index,
                                                                                               clazz["method_details"]))
        return file_detail_class_method_details % iter_string

    """
    This method generate the html doc string for the class' comment string.
    @version 1.0
    @author Benny
    @return the html doc string for the class' comment
    @param the hash map of class' comment
    """
    def generate_class_doc_string(self, comment):
        template_string = self.generate_doc_template("", comment)
        template = Template(template_string)
        return template.substitute(comment)

    """
    This method generate the html doc string for the functions' general
    @version 1.0
    @author Benny
    @return the html doc string for the functions' general
    @param the hash map of class' infomation
    """
    def file_detail_function_general_string(self, function):
        template_string = self.file_detail_function_general_template(function)
        substitute_map = {
            "_function_general": get_doc_string("_function_general"),
            "_function_general_table": get_doc_string("_function_general_table"),
            "_function": get_doc_string("_function"),
            "_param": get_doc_string("_param"),
        }
        num_function = self.count_procedure("function", function)
        substitute_map.update(function)
        substitute_map.update(self.COMMENT_MAP)
        for index in range(num_function):
            substitute_map["function%d_args" % (index + 1)] = self.generate_procedure_args_template("function" +
                                                                                                    str(index + 1),
                                                                                                    function)

        template = Template(template_string)
        return template.substitute(substitute_map)

    def file_detail_function_general_template(self, function):
        num_function = self.count_procedure("function", function)
        iter_string = ""

        for index in range(num_function):
            iter_string += file_detail_function_general_iter % (index % 2 and "altColor" or "rowColor", index + 1,
                                                                index + 1)

        return file_detail_function_general % iter_string

    """
    This method generate the html doc string for the functions' details
    @version 1.0
    @author Benny
    @return the html doc string for the functiions' details
    @param the hashmap of class' infomation
    """
    def file_detail_function_details_string(self, function):
        template_string = self.file_detail_function_details_template(function)
        substitute_map = {
            "_function_details": get_doc_string("_function_details"),
        }
        substitute_map.update(function)
        substitute_map.update(self.COMMENT_MAP)
        num_function = self.count_procedure("function", function)
        for index in range(num_function):
            substitute_map["function" + str(index + 1) + "_doc_text"] = ""
        for index in range(num_function):
            substitute_map["function%d_args" % (index + 1)] = self.generate_procedure_args_template("function" +
                                                                                                    str(index + 1),
                                                                                                    function)

        template = Template(template_string)
        return template.substitute(substitute_map)

    def file_detail_function_details_template(self, function):
        num_function = self.count_procedure("function", function)
        iter_string = ""

        for index in range(num_function):
            index += 1
            iter_string += file_detail_function_details_iter % (index, index, index, index,
                                                                self.generate_doc_template("function%d" % index,
                                                                                           function))

        return file_detail_function_details % iter_string

    """
    This method is a helper method of generating comment's template string(iterating).
    @version 1.0
    @author Benny
    @return the template string of comment
    @param the hash map of comment
    """
    @staticmethod
    def generate_doc_template(keyword, procedure_map):
        result_string = ""
        keyword += "_"
        for comment in procedure_map:
            comment_list = comment.split("_")
            if keyword in comment and comment_list[-1] in comment_string:
                result_string += comment_string[comment_list[-1]] % comment
        return result_string

    """
    This method generate the html doc string for the args of procedure
    @version 1.0
    @author Benny
    @param same as count_procudure
    @return the html doc string for the args of a procedure
    """
    @staticmethod
    def generate_procedure_args_template(keyword, map):
        result = ""
        for index, arg in enumerate(map):
            if keyword + "_arg" in arg:
                result += (index >= 1 and ", " or "") + map[arg]
        return result.strip(", ")

    """
    This method count the amount of a member in a class or file
    @version 1.0
    @author Benny
    @param same as count_procedure
    """
    @staticmethod
    def counter(keyword, map):
        num = 0
        for key in map:
            if keyword in key:
                num += 1
        return num

    """
    This method count the amount of procedure in a class or file
    @version 1.0
    @author Benny
    @param keyword of procedure, the hash map of file's or class' infomation
    """
    @staticmethod
    def count_procedure(keyword, map):
        num = 0
        procedure_name_list = []

        for key in map:
            procedure_name = key.split("_")[0]
            if not procedure_name in procedure_name_list:
                procedure_name_list.append(procedure_name)
                num += 1
        return num

    """
    This method generate the html doc string for the index file
    @version 1.0
    @author Benny
    @param file list
    @return the html doc string for the index file
    """
    @classmethod
    def generate_index(cls, file_list):
        iter_string = ""
        for index, file in enumerate(file_list):
            iter_string += package_index_file_list % (file, file)

        substitute_map = {
            "_all_files": get_doc_string("_all_files"),
            "file_list": iter_string,
        }
        template = Template(package_index_general)
        return template.substitute(substitute_map)

    """
    This method generate the html doc string for the main frame
    @version 1.0
    @author Benny
    @param file list
    @return the html doc string for the main frame
    """
    @classmethod
    def generate_main(cls, file_list):
        iter_string = ""
        for index, file in enumerate(file_list):
            iter_string += package_index_main_files % (index % 2 and "altColor" or "rowColor", file, file, file)

        substitute_map = {
            "_package": get_doc_string("_package"),
            "_file": get_doc_string("_file"),
            "_demostration": get_doc_string("_demostration"),
            "files": iter_string,
        }
        template = Template(package_index_main_general)
        return template.substitute(substitute_map)


"""
This function is used to test this module
@version 1.0
@author Benny
"""
def test():
    from lexer import Lexer
    from test import test_string, wrong_string
    from MapGenerator import MapGenerator
    from HTMLMapParser import HTMLMapParser

    try:
        print HTMLGenerator(HTMLMapParser(MapGenerator(Lexer(test_string)())(), "test")(), "test")()
    except GenerateError, e:
        e.write_error()
    except InvalidStringError, e:
        e.write_error()

if __name__ == "__main__":
    test()
