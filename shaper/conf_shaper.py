#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for input/output .properties, .xml, .yml, .json
"""
from __future__ import print_function, unicode_literals

import os
import sys
import json
from collections import OrderedDict
from io import StringIO
from xml.dom.minidom import parseString

import xmltodict
import dicttoxml
import oyaml as yaml

try:
    import ConfigParser
except:
    import configparser as ConfigParser


class ConfShaper(object):
    """ Class for input/output .properties, .xml, .yml, .json
    """

    def __init__(self, in_path, out_path):
        self.in_file_type = os.path.splitext(in_path)[1]
        self.out_file_type = os.path.splitext(out_path)[1]
        self.in_path = in_path
        self.out_path = out_path

    def read_file(self):
        """open file for read
        :return: object of the file type
        """
        try:
            config_fd = open(self.in_path, "r")
        except IOError as error:
            sys.exit("Input/Output error: {0}".format(error))
        except ValueError as error:
            sys.exit("program failed: Input/Output: {0}".format(error))
        except OSError as error:
            sys.exit("Bad file path {0}: {1}".format(self.out_path, error))
        return config_fd

    def write_file(self):
        """open file for write
        :return: object of the file type
        """
        try:
            outfile = open(self.out_path, 'w')
        except IOError as error:
            sys.exit("Input/Output error: {0}".format(error))
        except ValueError as error:
            sys.exit("program failed: Input/Output: {0}".format(error))
        except OSError as error:
            sys.exit("Bad file path {0}: {1}".format(self.out_path, error))
        return outfile

    def read_properties_file(self):
        """read ini properties"""
        properties_file = self.read_file()

        config = StringIO()
        config.write(u'[dummy_section]\n')
        try:
            config.write(properties_file.read().decode(
                encoding='UTF-8').replace('%', '%%'))
        except UnicodeError as error:
            sys.exit(
                "Unicode-related error: {}".format(error))
        config.seek(0, os.SEEK_SET)

        conf_parser = ConfigParser.SafeConfigParser()
        conf_parser.readfp(config)

        return OrderedDict(conf_parser.items('dummy_section'))

    def read_xml(self):
        """XML read

        :return: xml datastructure
        :rtype: OrderedDict
        """
        return xmltodict.parse(self.read_file())

    def read_yaml(self):
        """YAML read

        :return: yaml datastructure
        :rtype: OrderedDict
        """
        return yaml.load(self.read_file())

    def read_json(self):
        """JSON read

        :return: json datastructure
        :rtype: OrderedDict
        """
        return json.load(self.read_file(), object_pairs_hook=OrderedDict)

    def write_properties_file(self, data):
        """write kv ini like style"""
        properties_file = self.write_file()
        try:
            for key, value in data.items():
                properties_file.write(
                    "{}={}\n".format(key, value).encode(encoding='UTF-8')
                )
        except UnicodeError as error:
            sys.exit(
                "Unicode-related error: {}".format(error))

    def dump_xml(self, data):
        """write data to xml file
        """
        properties_file = self.write_file()
        dom = parseString(dicttoxml.dicttoxml(
            data, attr_type=False, root=False))
        try:
            properties_file.write(dom.toprettyxml(encoding="utf-8"))
        except UnicodeError as error:
            sys.exit(
                "Unicode-related error: {}".format(error))

    def dump_yaml(self, data):
        """Dump datastructure to yaml

        :param data: configuration dataset
        :type data: dict

        :return: None
        :rtype: None

        """
        yaml.dump(
            data,
            self.write_file(),
            default_flow_style=False,
            allow_unicode=True,
        )

    def dump_json(self, data):
        """write data to json file
        """
        stringj = json.dumps(data, indent=4, separators=(
            ',', ': '), encoding="utf-8")
        properties_file = self.write_file()
        try:
            properties_file.write(stringj.decode(
                "unicode-escape").encode(encoding='UTF-8'))
        except UnicodeError as error:
            sys.exit(
                "Unicode-related error: {}".format(error))

    def main(self):
        """main function - reads input file and write to output file
        """
        if self.in_file_type == ".xml":
            datastructure = self.read_xml()

        elif self.in_file_type == ".json":
            datastructure = self.read_json()

        elif self.in_file_type == ".yml":
            datastructure = self.read_yaml()

        elif self.in_file_type == ".properties":
            datastructure = self.read_properties_file()

        else:
            sys.exit("Unknown input file extension.")

        if self.out_file_type == ".xml":
            self.dump_xml(datastructure)

        elif self.out_file_type == ".json":
            self.dump_json(datastructure)

        elif self.out_file_type == ".yml":
            self.dump_yaml(datastructure)

        elif self.out_file_type == ".properties":
            self.write_properties_file(datastructure)

        else:
            sys.exit("Unknown output file extension.")

if __name__ == '__main__':
    #test xml
    SHAPER = ConfShaper("test.xml", "output.xml")
    print(SHAPER.in_file_type)
    SHAPER.main()

    SHAPER = ConfShaper("test.xml", "output.json")
    print(SHAPER.in_file_type)
    SHAPER.main()

    SHAPER = ConfShaper("test.xml", "output.yml")
    print(SHAPER.in_file_type)
    SHAPER.main()

    SHAPER = ConfShaper("test.xml", "output.properties")
    print(SHAPER.in_file_type)
    SHAPER.main()

    #test json
    SHAPER = ConfShaper("test.json", "output.xml")
    print(SHAPER.in_file_type)
    SHAPER.main()

    SHAPER = ConfShaper("test.json", "output.json")
    print(SHAPER.in_file_type)
    SHAPER.main()

    SHAPER = ConfShaper("test.json", "output.yml")
    print(SHAPER.in_file_type)
    SHAPER.main()

    SHAPER = ConfShaper("test.json", "output.properties")
    print(SHAPER.in_file_type)
    SHAPER.main()

    # test yml
    SHAPER = ConfShaper("test.yml", "output.xml")
    print(SHAPER.in_file_type)
    SHAPER.main()

    SHAPER = ConfShaper("test.yml", "output.json")
    print(SHAPER.in_file_type)
    SHAPER.main()

    SHAPER = ConfShaper("test.yml", "output.yml")
    print(SHAPER.in_file_type)
    SHAPER.main()

    SHAPER = ConfShaper("test.yml", "output.properties")
    print(SHAPER.in_file_type)
    SHAPER.main()

    #test properties
    SHAPER = ConfShaper("test.properties", "output.xml")
    print(SHAPER.in_file_type)
    SHAPER.main()

    SHAPER = ConfShaper("test.properties", "output.json")
    print(SHAPER.in_file_type)
    SHAPER.main()

    SHAPER = ConfShaper("test.properties", "output.yml")
    print(SHAPER.in_file_type)
    SHAPER.main()

    SHAPER = ConfShaper("test.properties", "output.properties")
    print(SHAPER.in_file_type)
    SHAPER.main()
