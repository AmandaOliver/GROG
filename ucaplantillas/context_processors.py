# coding: utf-8

import copy

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from main.conexion_bd import miembro_tiene_privilegios
from main.dni import username_to_dni


def navigation_context(request):
    """
    Este context_processor añade al contexto de las vistas los elementos de navegación definidos en el ajuste
    settings.NAVIGATION. Además, comprueba cuál es la URL actual y añade el elemento 'active' a los elementos coincidentes
    """

    # Primero, gestionamos los permisos: cada enlace puede indicar los grupos de usuarios que podrán verlo con el
    # elemento 'groups'. Si no existe este elemento todos los usuarios podrán ver el enlace
    nav = []

    # Guardamos los nombres de los grupos del usuario
    user_groups = [x.name for x in request.user.groups.all()]

    for element in settings.NAVIGATION:

        # Si el elemento de navegación no tiene restricción por grupos, se añade:
        if 'groups' not in element:
            nav.append(copy.deepcopy(element))

        # Si el usuario pertenece a alguno de los grupos permitidos, se añade
        elif set(user_groups) & set(element['groups']):
            nav.append(copy.deepcopy(element))

        # Si es administrador, se añade
        elif request.user.is_superuser:
            nav.append(copy.deepcopy(element))

    # Ahora todos los elementos que no tienen restriccion por grupos están en "nav",
    # asi que la recorremos buscando si tienen restriccion por seleccion de órgano
    nav2= []
    for element in nav:
        # si el elemento tiene restricción por órgano y éste no está seleccionado se saca de la lista
        if not (element.get('organo_requerido') == 'si' and request.session.get('organo') is None):
            nav2.append(element)
    nav = nav2
    nav2 = []
    if request.user.is_authenticated() and not request.user.is_superuser:
        dni = username_to_dni(request.user.username)
        organo = request.session.get('organo')
        for element in nav:
            #si el elemento necesita permisos especiales y el usuario es un miembro se saca de la lista
            if not (element.get('permiso_requerido') == 'si' and miembro_tiene_privilegios(dni, organo) is False):
                nav2.append(element)
        nav = nav2

    current_first_level = None
    current_second_level = None

    # Función en línea para comprobar si una cadena sin barras coincide con la ruta actual
    def matches(x):
        """
        Comprueba que la URL actual coincida con x. Tiene en cuenta el caso especial del home ("/")
        """

        if request.path == "/" and x == "/":
            return True
        elif x != "/" and request.path.startswith(x.rstrip('/')):
            return True
        else:
            return False

    # Recorremos todos los enlaces de navegación definidos
    for first_level_item in nav:

        # Si coincide el primer nivel, ponemos el atributo active a true
        if matches(first_level_item['url']):
            first_level_item['active'] = True
            current_first_level = first_level_item

        # Comprobamos si hay subnivel
        if 'items' not in first_level_item:
            continue

        # Recorremos subniveles
        for second_level_item in first_level_item['items']:
            if matches(second_level_item['url']):
                first_level_item['active'] = True
                second_level_item['active'] = True
                current_first_level = first_level_item
                current_second_level = second_level_item

            # Comprobamos si no hay un tercer subnivel
            if 'items' not in second_level_item:
                continue

            for third_level_item in second_level_item['items']:
                if third_level_item['url'] == request.path:
                    first_level_item['active'] = True
                    second_level_item['active'] = True
                    third_level_item['active'] = True
                    current_first_level = first_level_item
                    current_second_level = second_level_item

    return {
        'navigation': nav,
        'subnavigation': current_first_level['items'] if current_first_level and
                                                         'items' in current_first_level else None,
        'subsubnavigation': current_second_level['items'] if current_second_level and
                                                             'items' in current_second_level else None
    }
