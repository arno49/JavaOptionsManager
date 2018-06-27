#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Shaper (CMDB tool)
    Parse java properties to datastructure
    and create properties from datastructure.

    Support ivan.bogomazov@gmail.com
    Minsk 2018


    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    EXAMPLES:
        TBD
"""

from __future__ import print_function, unicode_literals

import argparse
import fnmatch
import os

from collections import OrderedDict

from shaper import lib
from shaper.lib.configi import FILE_TYPES


class Shaper(object):
    """Java options manager tool"""

    @staticmethod
    def walk_on_path(path):
        """recursive find files with pattern"""
        matches = []
        for pattern, _ in FILE_TYPES.items():
            for root, _dirnames, files in os.walk(path):
                for filename in fnmatch.filter(files, '*{}'.format(pattern)):
                    matches.append(os.path.join(root, filename))

        return matches

    @staticmethod
    def read_properties(path_to_dir):
        """interface for recursive read properties"""
        data = {}
        files = Shaper.walk_on_path(path_to_dir)

        for filename in files:
            data.update({
                filename: lib.read(filename)
            })

        return data

    @staticmethod
    def create_folders(path_to_folder):
        """recursive creating folders"""
        try:
            os.makedirs(path_to_folder)
        except OSError:
            if os.path.isdir(path_to_folder):
                pass
            else:
                raise EOFError

    @staticmethod
    def write_properties(datastructure, out_path):
        """interface for recursive write properties"""
        for filename, properties in datastructure.items():
            directories = os.path.join(
                out_path,
                os.path.dirname(filename)
            )
            property_file = os.path.basename(filename)
            Shaper.create_folders(directories)
            lib.write(
                os.path.join(
                    directories,
                    property_file
                ),
                properties
            )

    @staticmethod
    def forward_path_parser(_input):
        """parsing plain dict to nested"""

        def get_or_create_by_key(key, current_tree):
            """update dict by key"""
            if key not in current_tree:
                last = keys.pop()
                dict_update = {last: value}

                for _key in reversed(keys):
                    dict_update = {_key: dict_update}

                current_tree.update(dict_update)
            else:
                keys.pop(0)
                get_or_create_by_key(keys[0], current_tree[key])

        output = {}
        for key, value in OrderedDict(_input).items():
            keys = key.split('/')

            get_or_create_by_key(keys[0], output)

        return output

    @staticmethod
    def backward_path_parser(_input):
        """make nested structure plain"""

        def path_builder(current_tree, key=''):
            """make plain"""
            for _key, _value in current_tree.items():
                _key = key + '/' + _key if key else _key
                if '.' in _key:
                    output.update({_key: _value})
                else:
                    path_builder(_value, _key)

        output = {}
        path_builder(_input)

        return output


def parse_arguments():
    """Argument parsing

    :return: args namespace
    :rtype: namespace
    """
    parser = argparse.ArgumentParser(
        description='Tool to manage java properties'
    )

    parser.add_argument(
        "-v",
        dest="logging",
        action="count",
        default=0,
        help="Verbose output"
    )

    subparsers = parser.add_subparsers(
        dest="parser"
    )

    read = subparsers.add_parser(
        "read",
        help="Recursive read properties from files"
    )

    write = subparsers.add_parser(
        "write",
        help="Write properties files from datastructure"
    )

    read.add_argument(
        'src_path',
        type=str,
        help='Path to properties directory',
    )

    read.add_argument(
        '-o',
        '--out',
        dest='out',
        default='out.yml',
        help='Output file. Default out.yaml',
    )

    write.add_argument(
        "src_structure",
        type=str,
        help="Path to yaml with datastructure."
    )

    write.add_argument(
        '-o',
        '--out',
        dest='out',
        default='./out/',
        help='Path to output directory. Default ./out/',
    )

    write.add_argument(
        '-k',
        '--key',
        dest='key',
        default=None,
        help='Key for rendering custom subtree. Default render from root',
    )

    return parser.parse_args()


def play():
    """interface mock"""
    pass


def main():
    """main"""
    arguments = parse_arguments()
    shaper = Shaper()

    if arguments.parser == "read":
        tree = shaper.forward_path_parser(
            shaper.read_properties(
                arguments.src_path
            )
        )

        lib.write(arguments.out, tree)

    elif arguments.parser == "write":
        yaml_data = lib.read(arguments.src_structure)
        datastructure = shaper.backward_path_parser(yaml_data)

        # filter render files by key
        if arguments.key:
            datastructure = OrderedDict(
                (key, value)
                for key, value in datastructure.items()
                if arguments.key in key
            )

        if arguments.logging:
            print("==> Files to render :")
            print('\n'.join(datastructure.keys()))

        shaper.write_properties(datastructure, arguments.out)

    else:
        raise NotImplementedError


if __name__ == "__main__":
    main()
