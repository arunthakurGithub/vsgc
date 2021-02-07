from django import template
from django.template.defaulttags import register

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.simple_tag
def byte2str(key):
	if type(key) == str:
		return key
	return str(key.decode('UTF-8'))
