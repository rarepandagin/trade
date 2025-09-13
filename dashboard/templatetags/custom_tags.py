from django import template
from django.template.defaultfilters import stringfilter
import human_readable

register = template.Library()

from datetime import datetime

@register.filter()
@stringfilter
@register.simple_tag(takes_context=True)
def epoch_to_datetime(context, epoch_time):
    datetime_obj = datetime.fromtimestamp(epoch_time)
    return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')


@register.filter()
@stringfilter
@register.simple_tag(takes_context=True)
def time_delta_readable(context, epoch_time):
    datetime_obj = datetime.fromtimestamp(epoch_time)
    return human_readable.date_time(datetime.now() - datetime_obj)



@register.filter()
@stringfilter
@register.simple_tag(takes_context=True)
def auto_exit_style_filter(context, auto_exit_style):
    return ' '.join(auto_exit_style.split('_')[3:])

