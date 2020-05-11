from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.simple_tag
def get_total_actual_income(job, job_candidates):
    return intcomma(job.get_total_actual_income(job_candidates))
