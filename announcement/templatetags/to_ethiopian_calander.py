from django import template

from ethiopian_date import EthiopianDateConverter
from .ethiopian_months import ethiopian_months

register = template.Library()

@register.filter
def to_ethiopian(date):
    if not date:
        return ""

    converter = EthiopianDateConverter.date_to_ethiopian(date)
    year, month, day = converter.year,converter.month,converter.day
    month_name = ethiopian_months[month - 1]
    return f'{month_name} {day}, {year}'