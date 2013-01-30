# -*- coding: utf-8 -*-
from django.contrib.humanize.templatetags.humanize import intcomma
from django import template
register = template.Library()


@register.filter
def currency(total, part):
	if total:
		total = round(float(total), 2)
	else:
		total = round(0, 2)
	return "%s.%s" % (intcomma(int(total)), ("%0.2f" % total)[-2:])
