from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def sum_humanize(value):
    if value in (None, ""):
        return ""

    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return value

    amount = amount.normalize()
    if amount == amount.to_integral():
        return f"{int(amount):,}".replace(",", " ")

    integral, fractional = f"{amount:.2f}".split(".")
    integral_with_spaces = f"{int(integral):,}".replace(",", " ")
    return f"{integral_with_spaces}.{fractional}"