#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import fnmatch
import os
import yaml

from collections import defaultdict, OrderedDict

from shaper import lib
from shaper.lib.configi import FILE_TYPES
from shaper.manager import read_properties

from jinja2 import Environment, FileSystemLoader, Template


def generate_playbook(property_path):
    configs = read_properties(property_path)
    properties = defaultdict(list)
    for conf_file in configs:
        for property_name in configs[conf_file]:
            property_value = configs[conf_file][property_name]
            if property_value not in properties[property_name]:
                properties[property_name].append(property_value)
    global_vars = OrderedDict()
    for k, v in properties.items():
        if len(v) == 1:
            global_vars[k] = v[0]
    global_vars2 = OrderedDict(sorted(global_vars.items()))
    local_var = OrderedDict()
    for conf_file in configs:
        local_var[conf_file] = {}
        for property_name in configs[conf_file]:
            property_value = configs[conf_file][property_name]
            if property_name not in global_vars.keys():
                local_var[conf_file][property_name] = property_value
        new_local_var = OrderedDict(sorted(local_var[conf_file].items()))
        local_var[conf_file] = new_local_var
    new_local_var_2 = OrderedDict(sorted(local_var.items()))
    playbook = OrderedDict({'templates': ['globals.yml', 'locals.yml', 'custom.yml'],
                            'variables': {'global_vars': global_vars2,
                                          'local_vars': new_local_var_2}})
    with open('playbook.yml', 'w') as f:
        yaml.add_representer(OrderedDict,
                             lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))

        yaml.dump(playbook, f, default_flow_style=False)
    temp = OrderedDict()
    temp2 = OrderedDict()
    temp3 = OrderedDict()
    for conf_file in local_var.keys():
        temp[conf_file] = {}
        temp2[conf_file] = {}
        temp3[conf_file] = {}
        for var in local_var[conf_file].keys():
            temp[conf_file][var] = "{{ local_vars[\"%s\"][\"%s\"] }}" % (conf_file, var)
        temp_1 = OrderedDict(sorted(temp[conf_file].items()))
        temp[conf_file] = temp_1
        for var in global_vars.keys():
            temp2[conf_file][var] = "{{ global_vars[\"%s\"] }}" % var
        temp_2 = OrderedDict(sorted(temp2[conf_file].items()))
        temp2[conf_file] = temp_2
    new_temp = OrderedDict(sorted(temp.items()))
    new_temp2 = OrderedDict(sorted(temp2.items()))
    with open('globals.yml', 'w') as f:
        yaml.dump(new_temp2, f, default_flow_style=False)
    with open('locals.yml', 'w') as f:
        yaml.dump(new_temp, f, default_flow_style=False)
    with open('custom.yml', 'w') as f:
        yaml.dump(temp3, f, default_flow_style=False)


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


def merge_templates(rendered_templates, template_dir):
    dict_base = {}
    for template in rendered_templates:
        template = yaml.safe_load(template)
        for conf_name in template:
            if conf_name not in dict_base:
                dict_base[conf_name] = {}
            dict_base[conf_name].update(template[conf_name])
    return dict_base

