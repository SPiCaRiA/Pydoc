#!/usr/bin/python
#-*- coding=utf-8 -*-

import argparse

from localestring import get_help_string
from fileop import FileOp
from excepts import FileTypeError, FileNotFoundError


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help=get_help_string("file"))
    parser.add_argument("output", help=get_help_string("output"))
    args = parser.parse_args()

    try:
        FileOp(args.file, args.output)()
    except FileTypeError, e:
        e.write_error()
    except FileNotFoundError, e:
        e.write_error()


if __name__ == "__main__":
    main()
