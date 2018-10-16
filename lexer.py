#!/usr/bin/python
#-*- coding=utf-8 -*-

import re

from tokenmaps import token_exprs, syntax_exprs
from excepts import LexError


class Lexer():
    def __init__(self, token_stream):
        self.token_stream = token_stream

    def __call__(self):
        result = self.scan_file()
        return result

    """
    This method scan the file to get the comment and key member
    @version 1.0
    @author William
    @return the syntax parsed
    """
    def scan_file(self):
        position = 0
        character_sum = len(self.token_stream)
        result = []
        regex_split = re.compile(r",\s*")

        times = 0

        while position < character_sum:
            match = None
            for expr in syntax_exprs:
                pattern, flag = expr
                regex = flag and re.compile(pattern, re.M | re.S) or re.compile(pattern, re.M)
                match = regex.match(self.token_stream, position)
                if match:
                    position = match.end(0)

                    if flag:
                        if flag != "COMMENT":
                            syntax = (match.group(3), regex_split.split(match.group(4).strip("()")),
                                      match.group(2) and self.lex_comment(match.group(2), token_exprs,
                                      self.token_stream[:position].count("\n") + 1) or "", flag)
                            result.append(syntax)
                            break
                        else:
                            syntax = (match.group(1), flag)
                            result.append((self.lex_comment(match.group(1), token_exprs,
                                                           self.token_stream[:position].count("\n") + 1)
                                          , flag))
                            break
        return self.parse_syntax(result)

    """
    This is a helper method to get the type of the key member fetched
    @version 1.0
    @author William
    @param position of the member
    @return the type
    """
    def get_type(self, position):
        pattern = r"\n?(.+)\n"
        regex = re.compile(pattern)
        match = regex.match(self.token_stream, position)
        if match:
            text = match.group(1)
            if "class" in text:
                return "class"
            elif "def" in text:
                if "self" in text:
                    return "method"
                return "function"
        return "text"

    """
    This method is a tokenizer for lexing the comment
    @version 1.0
    @author William
    @param token stream, token expressions, line number
    @return list to represent the structure of the comment
    """
    def lex_comment(self, token_stream, token_exprs, line_no):
        if not token_stream:
            return ""
        position = 0
        tokens = []
        characters_sum = len(token_stream)

        while position < characters_sum:
            match = None
            for expr in token_exprs:
                pattern, flag = expr

                if flag == "TEXT":
                    regex = re.compile(pattern, re.S)
                else:
                    regex = re.compile(pattern)
                match = regex.match(token_stream, position)

                text = None
                if match:
                    if flag == "TAG":
                        text = (match.group(1), match.group(2)[1:])
                    elif flag == "TEXT":
                        text = match.group(1).rstrip()
                    token = text, flag
                    if not flag is None:
                        tokens.append(token)
                    position = match.end(0)
                    break

            if not match:
                regex_debug = re.compile("\n.*?%s.*\n" %
                        self.token_stream[position:self.token_stream.find("\n", position)])
                message = regex_debug.search(self.token_stream).group().strip()
                line = self.token_stream[:position].count("\n")
                raise LexError(message, line + line_no)

        return tokens

    """
    This method parse the list of tokens and organize them into an reasonable data structrue
    @version 1.0
    @author William
    @param tokens list
    @return the data structure parsed
    """
    def parse_syntax(self, syntax):
        comments = []
        comment = []

        classes = []

        funcs = []
        func = []

        for index, expr in enumerate(syntax):
            clazz = []
            if expr[-1] == "CLASS":
                methods = []
                cons = None
                for next_index in range(index + 1, len(syntax)):
                    if syntax[next_index][-1] == "METHOD" and syntax[next_index][0] == "__init__":
                        cons = syntax[next_index][:-1]
                    elif syntax[next_index][-1] == "METHOD" or syntax[next_index][-1] == "STATIC":
                        methods.append(syntax[next_index])
                    else:
                        break
                clazz.append([expr[:-1], cons, (methods, "METHOD")])

                classes.append(clazz)
            elif expr[-1] == "METHOD" or expr[-1] == "STATIC":
                continue
            elif expr[-1] == "COMMENT":
                comments.append(expr[0])
            elif expr[-1] == "FUNC":
                funcs.append(expr[:-1])

        if len(classes) == 0:
            classes.append([])

        comment.append(comments)
        comment.append("COMMENTS")
        classes.append("CLASSES")
        func.append(funcs)
        func.append("FUNCS")
        result = [comment, classes, func]
        return result


"""
This function is used to test this module
@version 1.0
@author William
"""
def test():
    from test import test_string
    filename = "test"
    try:
        print \
        Lexer(test_string)()
        # print Lexer(wrong_string)()
    except LexError, e:
        e.warning("test")

if __name__ == "__main__":
    test()


