import os
import sys
from .arpc import compiles


def print_help():
    text = """Usage: arpc [options] [value]
Options:
    -h, --help     output usage information
    -v, --version  output the version number

    -i, --input    input dir
    -o, --output   output dir
    -a, --async    async mode, default true
"""
    print(text)


def print_version():
    print("arpc-python version 0.1.0")


def main():
    args = sys.argv
    len_args = len(args)

    if len_args == 1:
        print("No args")
    elif len_args == 2:
        if args[1] == "--help" or args[1] == "-h":
            print_help()
        elif args[1] == "--version" or args[1] == "-v":
            print_version()
        else:
            print("Fatal error: Invalid args\n")
    elif len_args >= 5:
        input_ = ""
        output_ = ""
        async_ = False
        index = 1
        while index < len_args:
            if args[index] == "-i" or args[index] == "--input":
                input_ = args[index + 1]
            elif args[index] == "-o" or args[index] == "--output":
                output_ = args[index + 1]
            elif args[index] == "-a" or args[index] == "--async":
                if args[index + 1].lower() == "true":
                    async_ = True
            index += 2
        if input_ == "" or output_ == "":
            print("Fatal error: Invalid args\n")
        else:
            compiles(input_, output_, async_)
    else:
        print("Fatal error: Invalid args\n")
