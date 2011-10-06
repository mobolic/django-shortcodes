from shortcodes import parser
from django import template
register = template.Library()


def shortcodes_replace(value):
    return parser.parse(value)

register.filter('shortcodes', shortcodes_replace)
