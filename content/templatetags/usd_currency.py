from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter(name='usd_currency')
def usd_currency(value):
 
    if value > 0:
        value = round(value,2)
        checker = str(value)
        checker = checker[-2:]
        if checker != "00":
            value = intcomma(value)
        else:
            value = intcomma(value)[:-3]

        return f'${value}'
    else:
        return ''






