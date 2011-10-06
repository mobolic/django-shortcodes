import re
import shortcodes.parsers
from django.core.cache import cache


def import_parser(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def parse(value):
    ex = re.compile(r'\[(.*?)\]')
    groups = ex.findall(value)
    pieces = {}
    parsed = value

    for item in groups:
        if ' ' in item:
            name, space, args = item.partition(' ')
            args = __parse_args__(args)
        # If shortcode does not use spaces as a separator, it might use equals
        # signs.
        elif '=' in item:
            name, space, args = item.partition('=')
            args = __parse_args__(args)
        else:
            name = item
            args = {}

        item = re.escape(item)
        try:
            if cache.get(item):
                parsed = re.sub(r'\[' + item + r'\]', cache.get(item), parsed)
            else:
                module = import_parser('shortcodes.parsers.' + name)
                function = getattr(module, 'parse')
                result = function(args)
                cache.set(item, result, 3600)
                parsed = re.sub(r'\[' + item + r'\]', result, parsed)
        except ImportError:
            pass

    return parsed


def __parse_args__(value):
    ex = re.compile(r'[ ]*(\w+)=([^" ]+|"[^"]*")[ ]*(?: |$)')
    groups = ex.findall(value)
    kwargs = {}

    for group in groups:
        if group.__len__() == 2:
            item_key = group[0]
            item_value = group[1]

            if item_value.startswith('"'):
                if item_value.endswith('"'):
                    item_value = item_value[1:]
                    item_value = item_value[:item_value.__len__() - 1]

            kwargs[item_key] = item_value

    return kwargs
