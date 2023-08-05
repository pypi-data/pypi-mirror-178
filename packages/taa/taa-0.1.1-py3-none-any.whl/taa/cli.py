# -*- coding: utf-8 -*-

# @Software: PyCharm
# @File: cli.py
# @Author: xuefeng365
# @E-mail: 120158568@qq.com,
# @Site:
# @Time: 11月 23, 2022


import argparse
import sys

from taa import __description__, __version__
from taa.scaffold import init_parser_scaffold, main_scaffold


def main():
    # 命令行处理程序入口
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("-V", "--version", dest="version", action="store_true", help="show version")
    subparsers = parser.add_subparsers(help="sub-command help")
    sub_parser_scaffold = init_parser_scaffold(subparsers)

    if len(sys.argv) == 1:
        # taa
        parser.print_help()
        sys.exit(0)
    elif len(sys.argv) == 2:
        if sys.argv[1] in ["-V", "--version"]:
            # taa -V
            # taa --version
            print(f"{__version__}")
        elif sys.argv[1] in ["-h", "--help"]:
            # taa -h
            # taa --help
            parser.print_help()
        elif sys.argv[1] == "startproject":
            # taa startproject
            sub_parser_scaffold.print_help()
        sys.exit(0)

    args = parser.parse_args()


    if args.version:
        print(f"{__version__}")
        sys.exit(0)

    if sys.argv[1] == "startproject":
        # taa startproject project_name
        main_scaffold(args)
