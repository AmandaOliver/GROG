# -*- coding: utf-8 -*-
from django.utils import timezone
from datetimewidget.widgets import DateTimeWidget
from django import forms
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q

from multi_email_field.forms import MultiEmailField

from main.models import Punto, Reunion, Orden, Documentos
from main.settings import TIPOS_PUNTOS, ESTADO_PUNTOS


class CreatePuntoForm(forms.ModelForm):

    nombre_original = forms.CharField(label='Nombre')
    tipo_punto = forms.ChoiceField(label='Tipo de punto', choices=TIPOS_PUNTOS)
    requiere_elevacion = forms.BooleanField(label=u"¿Requiere ser elevado a aprobación o información del Consejo"
                                                  " de Gobierno?", required=False)
    # invitados = MultiEmailField(help_text='Introducir un email por línea, sin comas', required=False)
    comentarios = forms.CharField(label='Breve Descripción', widget=forms.Textarea, required=False)

    class Meta:
        model = Punto
        exclude = ['organo', 'nombre_admin', 'comentarios_admin', 'fecha_creacion', 'fecha_modificacion',
                   'creador', 'estado_punto', 'resolucion', 'estado_punto_anterior', 'consensuado_con']


class DocumentoForm(forms.ModelForm):
    documentos = forms.FileField(label='Documentos adjuntos', required=False)

    class Meta:
        model = Documentos
        fields = ('documentos', )


class UpdatePuntoForm(forms.ModelForm):
    nombre_original = forms.CharField(label='Nombre')
    tipo_punto = forms.ChoiceField(label='Tipo de punto', choices=TIPOS_PUNTOS)
    # invitados = MultiEmailField(help_text='Introducir un email por línea, sin comas', required=False)
    # estado_punto = forms.ChoiceField(label='Estado del punto', choices=ESTADO_PUNTOS)
    requiere_elevacion = forms.BooleanField(label=u"¿Requiere ser elevado a aprobación o información del Consejo"
                                                  " de Gobierno?", required=False)
    organo = forms.ChoiceField(label="Órgano")

    class Meta:
        model = Punto
        exclude = ['nombre_admin', 'comentarios_admin', 'fecha_creacion', 'fecha_modificacion',
                   'creador', 'resolucion', 'estado_punto_anterior', 'consensuado_con', 'estado_punto']

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('org')
        super(UpdatePuntoForm, self).__init__(*args, **kwargs)
        tuple(org)
        list_organos = []
        for o in org:
            list_organos.append((o, o),)
        self.fields['organo'].choices = list_organos



class UpdatePuntoResolucionForm(forms.ModelForm):
    class Meta:
        model = Punto
        fields = ['resolucion', 'estado_punto']




class UpdatePuntoSeguimientoForm(forms.ModelForm):
    class Meta:
        model = Punto
        fields = ['seguimiento']


class UpdateAdminPuntoForm(forms.ModelForm):
    readonly_fields = ('nombre_original', 'comentarios',)
    nombre_admin = forms.CharField(label='Nombre dado por el Secretario', required=False)
    comentarios_admin = forms.CharField(label='Comentarios del Secretario', widget=forms.Textarea, required=False)
    tipo_punto = forms.ChoiceField(label='Tipo de punto', choices=TIPOS_PUNTOS)
    # invitados = MultiEmailField(help_text='Introducir un email por línea, sin comas', required=False)
    estado_punto = forms.ChoiceField(label='Estado del punto', choices=ESTADO_PUNTOS)
    organo = forms.ChoiceField(label="Órgano")
    requiere_elevacion = forms.BooleanField(label=u"¿Requiere ser elevado a aprobación o información del Consejo"
                                                  " de Gobierno?", required=False)

    class Meta:
        model = Punto
        exclude = ['resolucion', 'creador', 'fecha_creacion', 'fecha_modificacion', 'estado_punto_anterior', 'consensuado_con']

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('org')
        super(UpdateAdminPuntoForm, self).__init__(*args, **kwargs)
        tuple(org)
        list_organos = []
        for o in org:
            list_organos.append((o, o),)
        self.fields['organo'].choices = list_organos
        for field in self.readonly_fields:
            self.fields[field].widget.attrs['readonly'] = True




class CreateReunionForm(forms.ModelForm):
    class Meta:
        model = Reunion
        exclude = ['fecha_creacion', 'creador', 'estado_reunion', 'organo', 'fecha_modificacion', 'asistentes',
                   'duracion_estimada']
        dateTimeOptions = {
            'format': 'dd/mm/yyyy hh:ii',
            'autoclose': True,
            'weekStart': 1,
            'todayHighlight': True
        }
        widgets = {
            # Use localization and bootstrap 3
            'fecha_hora': DateTimeWidget(attrs={'id': "fecha_hora"}, options=dateTimeOptions, bootstrap_version=3)
        }

    def clean_fecha_hora(self):
        fecha_hora = self.cleaned_data['fecha_hora']
        if fecha_hora <= timezone.now():
            raise ValidationError("La fecha no puede ser anterior a la de hoy.")
        return fecha_hora





# class UpdateReunionForm(forms.ModelForm):
#
#     organo = forms.ChoiceField(label="Órgano")
#     readonly_fields = ('estado_reunion', 'organo', 'duracion_estimada')
#     class Meta:
#         model = Reunion
#         exclude = ['fecha_creacion', 'creador', 'fecha_modificacion', 'asistentes']
#         dateTimeOptions = {
#             'format': 'dd/mm/yyyy hh:ii',
#             'autoclose': True,
#             'weekStart': 1,
#             'todayHighlight': True
#         }
#         widgets = {
#             # Use localization and bootstrap 3
#             'fecha_hora': DateTimeWidget(attrs={'id': "fecha_hora"}, options=dateTimeOptions, bootstrap_version=3)
#         }
#
#     def __init__(self, *args, **kwargs):
#         org = kwargs.pop('org')
#         super(UpdateReunionForm, self).__init__(*args, **kwargs)
#         tuple(org)
#         list_organos = []
#         for o in org:
#             list_organos.append((o, o),)
#         self.fields['organo'].choices = list_organos
#         for field in self.readonly_fields:
#             self.fields[field].widget.attrs['readonly'] = True
#

class OrganosForm(forms.Form):

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('org')
        super(OrganosForm, self).__init__(*args, **kwargs)
        tuple(org)
        list_organos = []
        for o in org:
            list_organos.append((o, o),)
        self.fields['organo'].choices = list_organos

    organo = forms.ChoiceField(label="Órgano")


class OrdenForm(forms.ModelForm):

    reunion = forms.HiddenInput()
    orden = forms.HiddenInput()

    class Meta:
        model = Orden
        fields = ('punto',)

    def __init__(self, *args, **kwargs):
        organo = kwargs.pop('organo')
        super(OrdenForm, self).__init__(*args, **kwargs)
        self.fields['punto'] = forms.ModelChoiceField(queryset=Punto.objects.filter(
            Q(organo=organo) & Q(Q(estado_punto='ST') | Q(estado_punto='TRAS'))).order_by('-fecha_modificacion'))
        self.fields['punto'].label = "Punto del día: "


