# coding: utf-8
from django.core.urlresolvers import reverse_lazy

NAVIGATION = [
    {'label': 'Inicio', 'url': reverse_lazy('home'), },
    {'label': 'Seleccionar Órgano', 'url': reverse_lazy('seleccion_organo')},
    {'label': 'Propuestas de Puntos', 'url': reverse_lazy('puntos_list'), 'organo_requerido': 'si', 'items': [
        {'label': 'Nueva propuesta', 'url': reverse_lazy('create_punto')},
    ]},
    {'label': 'Crear Reunión', 'organo_requerido': 'si', 'permiso_requerido': 'si', 'url': reverse_lazy('create_reunion')},
    {'label': 'Reuniones', 'url': reverse_lazy('reuniones_list'), 'organo_requerido': 'si'},
]

