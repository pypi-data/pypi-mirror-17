# Copyright (c) 2013 Alex Rudakov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from argparse import _HelpAction, _SubParsersAction
import re


class NavigationException(Exception):
    pass


def parser_navigate(parser_result, path, current_path=None):
    if isinstance(path, str):
        if path == '':
            return parser_result
        path = re.split('\s+', path)
    current_path = current_path or []
    if len(path) == 0:
        return parser_result
    if 'children' not in parser_result:
        raise NavigationException(
            'Current parser have no children elements.  (path: %s)' %
            ' '.join(current_path))
    next_hop = path.pop(0)
    for child in parser_result['children']:
        if child['name'] == next_hop:
            current_path.append(next_hop)
            return parser_navigate(child, path, current_path)
    raise NavigationException(
        'Current parser have no children element with name: %s  (path: %s)' % (
            next_hop, ' '.join(current_path)))


def _try_add_parser_attribute(data, parser, attribname):
    attribval = getattr(parser, attribname, None)
    if attribval is None:
        return
    if not isinstance(attribval, str):
        return
    if len(attribval) > 0:
        data[attribname] = attribval


def _format_usage_without_prefix(parser):
    """
    Use private argparse APIs to get the usage string without
    the 'usage: ' prefix.
    """
    fmt = parser._get_formatter()
    fmt.add_usage(parser.usage, parser._actions,
                  parser._mutually_exclusive_groups, prefix='')
    return fmt.format_help().strip()


def parse_parser(parser, data=None, **kwargs):
    if data is None:
        data = {
            'name': '',
            'usage': parser.format_usage().strip(),
            'bare_usage': _format_usage_without_prefix(parser),
            'prog': parser.prog,
        }
    _try_add_parser_attribute(data, parser, 'description')
    _try_add_parser_attribute(data, parser, 'epilog')
    for action in parser._get_positional_actions():
        if isinstance(action, _HelpAction):
            continue
        if isinstance(action, _SubParsersAction):
            helps = {}
            for item in action._choices_actions:
                helps[item.dest] = item.help

            # commands which share an existing parser are an alias,
            # don't duplicate docs
            subsection_alias = {}
            subsection_alias_names = set()
            for name, subaction in action._name_parser_map.items():
                if subaction not in subsection_alias:
                    subsection_alias[subaction] = []
                else:
                    subsection_alias[subaction].append(name)
                    subsection_alias_names.add(name)

            for name, subaction in action._name_parser_map.items():
                if name in subsection_alias_names:
                    continue
                subalias = subsection_alias[subaction]
                subaction.prog = '%s %s' % (parser.prog, name)
                subdata = {
                    'name': name if not subalias else
                            '%s (%s)' % (name, ', '.join(subalias)),
                    'help': helps.get(name, ''),
                    'usage': subaction.format_usage().strip(),
                    'bare_usage': _format_usage_without_prefix(subaction),
                }
                parse_parser(subaction, subdata, **kwargs)
                data.setdefault('children', []).append(subdata)
            continue
        if 'args' not in data:
            data['args'] = []
        arg = {
            'name': action.dest,
            'help': action.help or '',
            'metavar': action.metavar
        }
        if action.choices:
            arg['choices'] = action.choices
        data['args'].append(arg)
    show_defaults = (
        ('skip_default_values' not in kwargs)
        or (kwargs['skip_default_values'] is False))
    for action in parser._get_optional_actions():
        if isinstance(action, _HelpAction):
            continue
        if 'options' not in data:
            data['options'] = []
        option = {
            'name': action.option_strings,
            'default': action.default if show_defaults else '==SUPPRESS==',
            'help': action.help or ''
        }
        if action.choices:
            option['choices'] = action.choices
        if "==SUPPRESS==" not in option['help']:
            data['options'].append(option)
    return data
