#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import fnmatch
import os

from collections import OrderedDict

from shaper import lib
from shaper.lib.configi import FILE_TYPES

from jinja2 import Environment, FileSystemLoader


def render_template(template_path, context):
    """
    Render template interface

    :param template_path: path to template
    :type template_path: str

    :param context: variables
    :type context: dict

    :return: rendered template
    :rtype: str
    """
    env = Environment(
        loader=FileSystemLoader(
            os.path.dirname(template_path)
        )
    )
    env.globals.update(context)
    template = env.get_template(os.path.basename(template_path))
    return template.render()