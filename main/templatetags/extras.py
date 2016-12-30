# -*- coding: utf-8 -*-
import os
from django import template
from main.models import Reunion, Punto

register = template.Library()


@register.filter
def filename(value):
    return os.path.basename(value.file.name)


@register.simple_tag
def reunion_asistentes(pk):
    reunion = Reunion.objects.get(pk=pk)
    return str(reunion.asistentes).split(", ")

@register.simple_tag
def punto_consensuado(pk):
    punto= Punto.objects.get(pk=pk)
    return str(punto.consensuado_con).split(", ")

@register.filter
def filename(value):
    return os.path.basename(value.file.name)
