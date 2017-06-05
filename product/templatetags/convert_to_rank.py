from django import template
register = template.Library()

@register.filter(name='convert_to_rank')
def convert_to_rank(number):
    return range(1, number+1)
