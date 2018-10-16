#!/usr/bin/python
#-*- coding=utf-8 -*-

from excepts import ParseError


class MapGenerator():
    def __init__(self, tokens):
        self.tokens = tokens

    def __call__(self):
        result = self.generate_doc()
        return result

    """
    This method generate the doc content of the file
    @version 1.0
    @author Benny
    @return dict combined all the infomation in the file
    """
    def generate_doc(self):
        # [([('This is the message', 'TEXT')], 'text')]
        map = []
        try:
            map = self.parse_tokens()
        except ParseError, e:
            e.write_error()
        return map

    """
    This method use different method to parse the tokens into map
    @version 1.0
    @author William
    @return the list of map
    """
    def parse_tokens(self):
        classes = []
        funcs = []
        comments = []

        for token in self.tokens:
            if token[-1] == "COMMENTS":
                for comment in token[0]:
                    comments.append(self.generate_comment(comment))
            elif token[-1] == "CLASSES":
                for clazz in token[0]:
                    classes.append(self.generate_class(clazz))
            elif token[-1] == "FUNCS":
                for func in token[0]:
                    funcs.append(self.generate_func(func))
            else:
                raise ParseError
        return [classes, funcs, comments]

    """
    This method parse infomation of a class from lists and tuples into standard dict structure
    @version 1.0
    @author Benny
    @return dict parsed from a class infomation list
    """
    def generate_class(self, tokens):
        map = {
            "name": "",
            "super": "",
            "comment": "",

            "cons name": "",
            "cons args": "",
            "cons comment": "",

            "methods": "",
        }
        map = tokens[0] and self.generate_classinfo(map, tokens[0]) or map
        map = tokens[1] and self.generate_consinfo(map, tokens[1]) or map
        map = tokens[2] and self.generate_methodinfo(map, tokens[2]) or map
        return map

    def generate_classinfo(self, map, clazz):
        map["name"] = clazz[0] and clazz[0] or ""
        map["super"] = clazz[1] and clazz[1] or ""
        map["comment"] = clazz[2] and self.generate_comment(clazz[2]) or ""
        return map

    def generate_consinfo(self, map, cons):
        map["cons name"] = cons[0] and cons[0] or ""
        map["cons args"] = cons[1] and cons[1] or ""
        map["cons comment"] = cons[2] and self.generate_comment(cons[2]) or ""
        return map

    def generate_methodinfo(self, map, methods):
        map["methods"] = methods[0] and self.generate_methods(methods[0]) or ""


    """
    This method parse infomation of a function from lists and tuples into standard dict structure
    @version 1.0
    @author Benny
    @return dict parsed from a function's infomation lists
    """
    def generate_func(self, tokens):
        map = {
            "name": tokens[0] and tokens[0] or "",
            "args": tokens[1] and tokens[1] or "",
            "comment": tokens[2] and self.generate_comment(tokens[2]) or "",
        }
        return map


    """
    This method parse comment from lists and tuples into standard dict structure
    @author Benny
    @version 1.0
    @return dict parsed from comment token list
    """
    def generate_comment(self, tokens):
        if not tokens:
            return ""
        map = {
            "text": self.find_tag("TEXT", tokens),

            "version": self.find_tag("version", tokens),
            "author": self.find_tag("author", tokens),
            "since": self.find_tag("since", tokens),
            "param": self.find_tag("param", tokens),
            "return": self.find_tag("return", tokens),
            "throws": self.find_tag("throws", tokens),
        }
        return map

    def find_tag(self, tag_name, tokens):
        for token in tokens:
            if token[-1] == tag_name:
                return token[0]
            elif token[0][0] == tag_name:
                return token[0][1]
        return ""


    """
    This method parse methods infomation from lists and tuples into standard dict structure
    @version 1.0
    @author Benny
    @return dict parsed from methods infomation list
    """
    def generate_methods(self, methods):
        result = []
        for method in methods:
            map = {
                "name": "",
                "args": "",
                "comment": "",
            }
            map = method[0] and self.generate_method_name(map, method[0]) or map
            map = method[1] and self.generate_method_args(map, method[1]) or map
            map = method[2] and self.generate_method_comments(map, method[2]) or map
            result.append(map)
        return result

    def generate_method_name(self, map, method_name):
        map["name"] = method_name and method_name or ""
        return map

    def generate_method_args(self, map, args):
        map["args"] = args and args or ""
        return map

    def generate_method_comments(self, map, comments):
        map["comment"] = comments and self.generate_comment(comments) or ""


def test():
    from lexer import Lexer
    from test import test_string, wrong_string

    print MapGenerator(Lexer(wrong_string)())()
    # print MapGenerator(Lexer(wrong_string)())()

if __name__ == "__main__":
    test()
