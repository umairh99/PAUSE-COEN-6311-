from django import template

register = template.Library()

@register.filter
def values(queryset):
    return queryset.values_list('id', flat=True)
