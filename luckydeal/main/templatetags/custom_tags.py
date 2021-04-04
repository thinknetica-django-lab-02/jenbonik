from django import template
from django.template.defaultfilters import stringfilter

import datetime

register = template.Library()

@register.filter
@stringfilter
def invert(value: str) -> str:
    """Инвертирует строку"""
    return value[::-1]


@register.filter
def dec(number: int) -> int:
    """ Декремент значения """
    return number - 1


@register.simple_tag
def server_date_time(format_string: str) -> str:
    """ Время сервера """
    return datetime.datetime.now().strftime(format_string)
