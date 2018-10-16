#!/usr/bin/python
#-*- coding=utf-8 -*-


class HTMLMapParser():
    def __init__(self, map, filename):
        self.map = map
        self.filename = filename

    def __call__(self):
        result = self.parse_map()
        return result

    def parse_map(self):
        result = {}
        for index, clazz in enumerate(self.map[0]):
            result["class" + str(index + 1)] = self.parse_classes_map(clazz)

        result["function_general"] = {}
        result["function_general"].update(self.parse_procedures_map(self.map[1], "function"))

        result["function_details"] = result["function_general"]

        result["filename"] = self.filename

        if self.map[2]:
            result.update(self.parse_filedoc_map(self.map[2][0]))

        return result

    def parse_fileinfo_map(self):
        pass

    def parse_filedoc_map(self, comment):
        result = {}
        if not comment:
            return result
        for key, value in comment.iteritems():
            if value:
                result["file_doc_" + key] = value
        return result

    def parse_classes_map(self, clazz):
        if not clazz:
            return {}

        clazz_info = {}
        clazz_info["class_name"] = clazz["name"]
        clazz_info["super"] = self.parse_class_super_map(clazz["super"])
        clazz_info["class_comment"] = self.parse_class_comment_map(clazz["comment"])
        clazz_info["method_general"] = self.parse_procedures_map(clazz["methods"], "method")
        clazz_info["cons_general"] = self.parse_cons_map(clazz)
        clazz_info["cons_details"] = clazz_info["cons_general"]
        clazz_info["method_details"] = clazz_info["method_general"]

        return clazz_info

    def parse_class_comment_map(self, comment):
        result = {}
        if not comment:
            return result

        for key, value in comment.iteritems():
            if value:
                result["class_doc_" + key] = value
        return result

    def parse_class_super_map(self, supers):
        result = {}
        for index, super in enumerate(supers):
            result["super" + str(index + 1)] = super
        return result

    def parse_cons_map(self, clazz):
        result = {}
        if not clazz:
            return result
        result.update(self.parse_args_map(clazz["cons args"], "cons"))
        result.update(self.parse_procedure_comment_map(clazz["cons comment"], "cons"))
        return result

    def parse_procedures_map(self, procedures, mode):
        result = {}
        if not procedures:
            return result

        for index, procedure in enumerate(procedures):
            if not procedure:
                return result

            result[mode + str(index + 1) + "_name"] = procedure["name"]
            result.update(self.parse_args_map(procedure["args"], mode, index + 1))
            result.update(self.parse_procedure_comment_map(procedure["comment"], mode, index + 1))
        return result

    @staticmethod
    def parse_args_map(args, mode, num=1):
        result = {}
        if not args:
            return result

        for index, arg in enumerate(args):
            if mode == "cons":
                result[mode + "_arg" + str(index + 1)] = arg
            else:
                result[mode + str(num) + "_arg" + str(index + 1)] = arg
        return result

    @staticmethod
    def parse_procedure_comment_map(comment, mode, num=1):
        result = {}
        if not comment:
            return result

        for key, value in comment.iteritems():
            if value and mode == "cons":
                result[mode + "_doc_" + key] = value
            elif value:
                result[mode + str(num) + "_doc_" + key] = value
        return result


def test():
    from lexer import Lexer
    from test import test_string, wrong_string
    from MapGenerator import MapGenerator

    print HTMLMapParser(MapGenerator(Lexer(test_string)())(), "test")()

if __name__ == "__main__":
    test()
