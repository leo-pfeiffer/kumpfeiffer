# https://hakibenita.medium.com/hey-52138a2949a8

from django import template

register = template.Library()


@register.filter()
def divide(n1, n2):
    try:
        return n1 / n2
    except ZeroDivisionError:
        return None


@register.filter()
def multiply(n1, n2):
    return n1 * n2


@register.filter()
def percentof(amount, total):
    try:
        return "{:.1f}%".format(amount / total * 100)
    except ZeroDivisionError:
        return None


@register.filter()
def dict_key(d, k):
    return d.get(k)


@register.filter()
def form_field(f, k):
    return f.__getitem__(k)
