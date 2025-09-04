from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

from datetime import datetime

@register.filter()
@stringfilter
@register.simple_tag(takes_context=True)
def epoch_to_datetime(context, epoch_time):
    datetime_obj = datetime.fromtimestamp(epoch_time)
    return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

