#!/usr/bin/python
#-*- coding=utf-8 -*-

test_string = \
 """'''
this is the file annotation
@author Linus
@version 1.0
@since 0.5
'''
'''
nooo
'''
class C(object, Super):
    '''
    half-caste symphony
    @param the object itself
    '''
    def __init__(self):
        print 'a'

    def a_method(self, str):
        print str
    '''
    @param No parameter
    @return No return value
    '''
    @staticmethod
    def print_static():
        print 'static'
'''
This is the procedure yeah
@param str1 and str2 to be printed
@return No return value
'''
def function(str1, str2):
    print 'func'
def function2(int1):
    print 'func2'
 """

# wrong_string = \
# """'''
# Test text annotation
# @author rundis
# @version 1.0
# @throws SyntaxError
# @return returnValue
# @param param1, param2
# '''
# class test():
#     a
#     a
#     a
#     a
# '''
# ccc
# '''
# '''
# aaa
# '''
# """

wrong_string = \
"""
print 'hello'
"""