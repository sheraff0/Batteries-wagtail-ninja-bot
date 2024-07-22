from functools import wraps

from django.contrib.humanize.templatetags.humanize import intcomma as intcomma_filter
from django.utils.html import format_html


def style_text(text, attr_key, attr_value):
    return format_html(f'<span style="{attr_key}: {attr_value};">{text}</span>')


def color_text(text, color):
    return style_text(text, "color", color)


def mark_validated(
    validators: list[object],
    color_clean: str = "green",
    color_fail: str = "red",
):
    def __(func):
        @wraps(func)
        def _(*args, **kwargs):
            res = None
            try:
                res = func(*args, **kwargs)
                for validator in validators:
                    assert validator(res)
                return color_text(res, color_clean)
            except Exception as e:
                print(e)
                return color_text(res, color_fail)
        return _
    return __


def decorate(value, decorator, default=None, validators=list()):
    try:
        assert value is not None
        for validator in validators:
            assert validator(value)
        _value = decorator(value)
        return _value
    except:
        return default


def intcomma(value):
    return decorate(value, intcomma_filter, default=format_html("&nbsp;"), validators=[lambda x: x != 0])
