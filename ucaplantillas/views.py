# coding: utf-8
from django.shortcuts import render
from django.contrib import messages


def ejemplo(request):
    """
    Ejemplo
    """
    # un simple mensaje de ejemplo para ver como queda en la plantilla
    messages.add_message(request, messages.SUCCESS, 'Cambios guardados correctamente.')

    return render(request, 'ejemplo/ejemplo.html')
