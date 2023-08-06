import re
from fnmatch import fnmatch
from invisibleroads_macros.configuration import (
    RawCaseSensitiveConfigParser, load_settings, unicode_safely)
from invisibleroads_macros.disk import are_same_path
from os import getcwd, walk
from os.path import abspath, basename, dirname, isabs, join
from pyramid.settings import asbool, aslist

from .exceptions import (
    ToolConfigurationNotFound, ToolNotFound, ToolNotSpecified)


TOOL_NAME_PATTERN = re.compile(r'crosscompute\s*(.*)')
ARGUMENT_NAME_PATTERN = re.compile(r'\{(.+?)\}')


def find_tool_definition_by_name(folder, default_tool_name=None):
    tool_definition_by_name = {}
    folder = unicode_safely(folder)
    default_tool_name = unicode_safely(default_tool_name)
    for root_folder, folder_names, file_names in walk(folder):
        if are_same_path(root_folder, folder):
            tool_name = default_tool_name or basename(folder)
        else:
            tool_name = basename(root_folder)
        for file_name in file_names:
            if not fnmatch(file_name, '*.ini'):
                continue
            tool_definition_by_name.update(load_tool_definition_by_name(
                join(root_folder, file_name),
                default_tool_name=tool_name))
    return tool_definition_by_name


def find_tool_definition(folder=None, tool_name='', default_tool_name=''):
    tool_definition_by_name = find_tool_definition_by_name(
        folder or getcwd(), default_tool_name)
    if not tool_definition_by_name:
        raise ToolConfigurationNotFound(
            'Tool configuration not found. Run this command in a folder '
            'with a tool configuration file or in a parent folder.')
    if len(tool_definition_by_name) == 1:
        return list(tool_definition_by_name.values())[0]
    if not tool_name:
        raise ToolNotSpecified('Tool not specified. %s' % (
            format_available_tools(tool_definition_by_name)))
    tool_name = tool_name or tool_definition_by_name.keys()[0]
    try:
        tool_definition = tool_definition_by_name[tool_name]
    except KeyError:
        raise ToolNotFound('Tool not found (%s). %s' % (
            tool_name, format_available_tools(tool_definition_by_name)))
    return tool_definition


def load_tool_definition_by_name(
        tool_configuration_path, default_tool_name=None):
    tool_definition_by_name = {}
    tool_configuration_path = abspath(tool_configuration_path)
    tool_configuration = RawCaseSensitiveConfigParser()
    tool_configuration.read(tool_configuration_path)
    d = {
        u'configuration_path': tool_configuration_path,
        u'configuration_folder': dirname(tool_configuration_path),
    }
    for section_name in tool_configuration.sections():
        try:
            tool_name = TOOL_NAME_PATTERN.match(section_name).group(1).strip()
        except AttributeError:
            continue
        if not tool_name:
            tool_name = default_tool_name
        tool_definition = {
            unicode_safely(k): unicode_safely(v)
            for k, v in tool_configuration.items(section_name)}
        for key in tool_definition:
            if key.startswith('show_'):
                tool_definition[key] = asbool(tool_definition[key])
            elif key.endswith('.dependencies'):
                tool_definition[key] = aslist(tool_definition[key])
        tool_definition[u'tool_name'] = tool_name
        tool_definition[u'argument_names'] = parse_tool_argument_names(
            tool_definition.get('command_template', u''))
        tool_definition_by_name[tool_name] = dict(tool_definition, **d)
    return tool_definition_by_name


def load_tool_definition(result_configuration_path):
    s = load_settings(result_configuration_path, 'tool_definition')
    tool_configuration_path = s['configuration_path']
    tool_name = s['tool_name']
    if not isabs(tool_configuration_path):
        result_configuration_folder = dirname(result_configuration_path)
        tool_configuration_path = join(
            result_configuration_folder, tool_configuration_path)
    return load_tool_definition_by_name(tool_configuration_path, tool_name)[
        tool_name]


def load_result_arguments(result_configuration_path):
    result_arguments = {}
    result_configuration_folder = dirname(abspath(result_configuration_path))
    for k, v in load_settings(
            result_configuration_path, 'result_arguments').items():
        if k == 'target_folder':
            continue
        if (k.endswith('_path') or k.endswith('_folder')) and not isabs(v):
            v = join(result_configuration_folder, v)
        result_arguments[k] = v
    return result_arguments


def format_available_tools(tool_definition_by_name):
    tool_count = len(tool_definition_by_name)
    return '%s available:\n%s' % (
        tool_count, '\n'.join(tool_definition_by_name))


def parse_tool_argument_names(command_template):
    return tuple(ARGUMENT_NAME_PATTERN.findall(command_template))
