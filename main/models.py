# coding: utf-8

from __future__ import unicode_literals

import os
from datetime import timedelta
from datetime import datetime
from django.core.urlresolvers import reverse
from multi_email_field.fields import MultiEmailField

from GROG import settings
from main.settings import TIPOS_PUNTOS, ESTADO_PUNTOS, INFORMACION, SIN_TRATAR, ESTADO_REUNIONES, CREADA
from django.contrib.auth.models import User
from django.db import models

class Punto(models.Model):
    organo = models.CharField(max_length=255)
    nombre_original = models.CharField(max_length=1500)
    nombre_admin = models.CharField(max_length=1500, null=True, blank=True)  # copia del original
    comentarios = models.TextField(blank=True, default="")
    comentarios_admin = models.TextField(blank=True, default="")
    tipo_punto = models.CharField(max_length=4, choices=TIPOS_PUNTOS, default=INFORMACION)
    requiere_elevacion = models.BooleanField(null=False, default=False)
    duracion_estimada = models.DurationField(default=timedelta(minutes=20))
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado_punto = models.CharField(max_length=4, choices=ESTADO_PUNTOS, default=SIN_TRATAR)
    estado_punto_anterior = models.CharField(max_length=4, choices=ESTADO_PUNTOS, blank=True)
    creador = models.ForeignKey(settings.AUTH_USER_MODEL)
    # invitados = MultiEmailField(null=True, blank=True)
    resolucion = models.TextField(null=True, blank=True)
    consensuado_con = models.TextField(blank=True, null=True)
    seguimiento = models.TextField(blank=True, null=True)


    def __unicode__(self):
        return self.nombre_original

    def get_absolute_url(self):
        return reverse('punto_detail', kwargs={'pk': self.pk})

    def clean(self):
        """
        hace que el campo nombre_admin sea copia de nombre_original si se deja en blanco
        """
        self.nombre_admin = self.nombre_original


class Documentos(models.Model):
    punto = models.ForeignKey(Punto)
    documento = models.FileField(upload_to='uploads/%Y%m%d%H%M%S', null=True, blank=True)  # para varios en el form

    def __unicode__(self):
        return unicode(self.id)

class Reunion(models.Model):
    fecha_hora = models.DateTimeField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    lugar = models.CharField(max_length=300)
    organo = models.CharField(max_length=255)
    creador = models.ForeignKey(settings.AUTH_USER_MODEL)
    # acta generada automaticamente a partir de la redacción de los puntos
    duracion_estimada = models.DurationField(blank=True, null=True)
    estado_reunion = models.CharField(max_length=4, choices=ESTADO_REUNIONES, default=CREADA)
    asistentes = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.fecha_hora)

    def get_absolute_url(self):
        return reverse('reunion_detail', kwargs={'pk': self.pk})


class Orden(models.Model):
    reunion = models.ForeignKey(Reunion)
    punto = models.ForeignKey(Punto)
    orden = models.IntegerField()
