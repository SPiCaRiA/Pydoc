#!/usr/bin/python
#-*- coding=utf-8 -*-

TAG = "TAG"
TEXT = "TEXT"

COMMENT = "COMMENT"
FUNC = "FUNC"
METHOD = "METHOD"
CLASS = "CLASS"
STATIC = "STATIC"

token_exprs = [
            (r"\s+", None),

            (r"'''", None),

            (r"@(version)(.*)", TAG),
            (r"@(author)(.*)", TAG),
            (r"@(since)(.*)", TAG),
            (r"@(param)(.*)", TAG),
            (r"@(return)(.*)", TAG),
            (r"@(throws)(.*)", TAG),

            ("([^@]+)", TEXT),
        ]

syntax_exprs = [
            (r"\s+$", None),

            (r"\s*([\"']{3}\s+(.+?)\s+[\"']{3}\s*)?"
             r"\s*@staticmethod\s+"
             r"def\s+(.+?)\s*(\((.*?)\))\s*:", STATIC),
            (r"\s*([\"']{3}\s+(.+?)\s+[\"']{3}\s*)?"
             r"\s*@classmethod\s+"
             r"def\s+(.+?)\s*(\((.*?)\))\s*:", STATIC),
            (r"\s*([\"']{3}\s+(.+?)\s+[\"']{3}\s*)?"
             r"\s*def\s+(.+?)\s*(\(self\s*,?\s*(.*?)\))\s*:", METHOD),
            (r"\s*([\"']{3}\s+(.+?)\s+[\"']{3}\s*)?"
             r"\s*\s*def\s+(.+?)\s*(\((.*?)\))\s*:", FUNC),
            (r"\s*([\"']{3}\s+(.+?)\s+[\"']{3}\s*)?"
             r"\s*class\s+(.+?)\s*(\((.*?)\))?\s*:", CLASS),

            (r"^[\"']{3}\s+(.+?)\s+[\"']{3}\s*", COMMENT),

            (".*?\n", None),
        ]

if __name__ == "__main__":
    for pattern, flag in token_exprs:
        print pattern, flag

    for pattern, flag in syntax_exprs:
        print pattern, flag
