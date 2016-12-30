from django import template

register = template.Library()


@register.filter
def verbose_name(value):
    """
    Filtro para su uso en templates que devuelve el verbose_name de un modelo. Por ejemplo:

        {{ object|verbose_name }}
    """
    return value._meta.verbose_name


@register.filter
def verbose_name_plural(value):
    """
    Filtro para su uso en templates que devuelve el verbose_name_plural de un modelo. Por ejemplo:

        {{ object|verbose_name_plural }}
    """
    return value._meta.verbose_name_plural


