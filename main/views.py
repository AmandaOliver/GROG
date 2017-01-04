# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import re
from datetime import timedelta
from django.template.defaultfilters import date as _date
import sys

from django.core.urlresolvers import reverse_lazy
from django.db.models.query_utils import Q

from django.forms.models import modelformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import View, DetailView, DeleteView, TemplateView

from main.dni import username_to_dni
from main.forms import CreatePuntoForm, UpdatePuntoForm, CreateReunionForm, OrganosForm, \
    UpdateAdminPuntoForm, UpdatePuntoResolucionForm, UpdatePuntoSeguimientoForm, DocumentoForm, OrdenForm
from main.models import Punto, Reunion, Documentos, Orden
from main.conexion_bd import organos_miembro, miembro_tiene_privilegios, lista_miembros_organo, \
    lista_miembros_organo_email
from django.core.mail import EmailMessage


# Vista de Home
class HomeView(TemplateView):
    template_name = "main/home.html"


# Vista de Selección de Órgano
class SeleccionOrganoView(View):
    @staticmethod
    def post(request):
        """
        Esta función devuelve una página con un formulario donde escoger el órgano
        :param request: HttpRequest
        :return: HttpResponse
        """
        dni = username_to_dni(request.user.username)
        form = OrganosForm(request.POST, org=organos_miembro(dni))
        if form.is_valid():
            organo = form.cleaned_data['organo']
            request.session['organo'] = organo
            return redirect('puntos_list')

    @staticmethod
    def get(request):
        # type: (object) -> object
        if re.match(r'u[0-9]{8}', request.user.username):
            dni = username_to_dni(request.user.username)
            form = OrganosForm(org=organos_miembro(dni))
            if request.session._session.get(u'organo'):
                context = {
                    'form': form,
                    'organo_actual': request.session._session.get(u'organo')
                }
            else:
                context = {
                    'form': form
                }
            return render(request, 'main/organo_selec.html', context)
        else:
            return render(request, 'main/usuario_no_valido.html')


# Vistas de Puntos
class PuntoCreateView(View):

    def get(self, request):
        DocumentosFormSet = modelformset_factory(Documentos, form=DocumentoForm, extra=1)
        form = CreatePuntoForm()
        formset = DocumentosFormSet(queryset=Documentos.objects.none())
        context = {
            'form': form,
            'formset': formset
        }
        return render(request, 'main/create_punto.html', context)

    def post(self, request):
        DocumentosFormSet = modelformset_factory(Documentos, form=DocumentoForm, extra=1)
        form = CreatePuntoForm(request.POST)
        formset = DocumentosFormSet(request.POST, request.FILES, queryset=Documentos.objects.none())

        if form.is_valid() and formset.is_valid():
            punto = form.save(commit=False)
            punto.creador = self.request.user
            punto.organo = self.request.session.get('organo')
            punto.save()
            for form in formset.cleaned_data:
                if form.get('documentos') is not None:
                    documento = form.get('documentos')
                    doc = Documentos(punto=punto, documento=documento)
                    doc.save()

            return redirect(reverse_lazy('punto_consensuado', kwargs={'pk': punto.pk}))
        return render_to_response('main/create_punto.html', {'form': form, 'formset': formset})




class PuntoConsensuadoView(View):

    def get(self, request, pk):
        reload(sys)
        sys.setdefaultencoding('UTF8')
        punto = Punto.objects.get(pk=pk)
        if request.GET.get('add'):
            self.add_miembro_consensuado(request.GET.get('miembro'), punto)
            request.GET.get == ""
            return redirect(reverse_lazy('punto_consensuado', kwargs={'pk': punto.pk}))
        if request.GET.get('delete'):
            self.delete_miembro_consensuado(request.GET.get('miembro2'), punto)
            request.GET.get == ""
            return redirect(reverse_lazy('punto_consensuado', kwargs={'pk': punto.pk}))

        context = {
            'miembros': lista_miembros_organo(self.request.session.get('organo')),
            'punto': punto,
        }
        return render(request, 'main/punto_consensuado.html', context)

    def add_miembro_consensuado(self, miembro, punto):
        if punto.consensuado_con is None:
            aux = []
        else:
            aux = str(punto.consensuado_con).split(", ")
        aux.append(miembro)
        punto.consensuado_con = ", ".join(aux)
        punto.save()

    def delete_miembro_consensuado(self, miembro, punto):
        aux = str(punto.consensuado_con).split(", ")
        aux.remove(miembro)
        punto.consensuado_con = ", ".join(aux)
        punto.save()


class PuntoDetailView(DetailView):
    model = Punto
    template_name = "main/punto_detail.html"

    def usuario_tiene_permiso(self):
        dni = username_to_dni(self.request.user.username)
        organo = self.request.session.get('organo')
        return miembro_tiene_privilegios(dni, organo)

    def documentos_list(self):
        punto = self.get_object()
        documentos = Documentos.objects.filter(punto=punto)
        if not documentos:
            return "None"
        else:
            return documentos



class PuntoUpdateView(View):

    def get_object(self, queryset=None, pk=None):
        obj = Punto.objects.get(id=self.kwargs['pk'])
        if obj.estado_punto == 'ST':
            return obj
        else:
            return None

    def get(self, request, pk):
        dni = username_to_dni(request.user.username)
        punto = self.get_object(Punto, pk=pk)
        form = UpdatePuntoForm(instance=punto, org=organos_miembro(dni))
        queryset = Documentos.objects.filter(punto=punto)
        context = {
            'form': form,
            'punto': punto,
            'tipo': "general"
        }
        return render(request, 'main/punto_update.html', context)

    def post(self, request, pk):
        punto = self.get_object(Punto, pk=pk)
        queryset = Documentos.objects.filter(punto=punto)
        dni = username_to_dni(request.user.username)
        form = UpdatePuntoForm(request.POST, instance=punto, org=organos_miembro(dni))
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('punto_consensuado', kwargs={'pk': punto.pk}))
        return render(request, 'main/punto_update.html', {'form': form, 'punto': punto, 'tipo': "general",
                                                          })


class PuntoUpdateResolucionView(View):
    def get_object(self, queryset=None, pk=None):
        obj = Punto.objects.get(id=self.kwargs['pk'])
        if obj.estado_punto == 'CONV':
            return obj
        else:
            return None

    def get(self, request, punto_pk, reunion_pk):
        punto = self.get_object(Punto, pk=punto_pk)
        form = UpdatePuntoResolucionForm(instance=punto)
        context = {
            'form': form,
            'tipo': "resolucion"
        }
        return render(request, 'main/punto_update.html', context)

    def post(self, request, punto_pk, reunion_pk):
        punto = Punto.objects.get(pk=punto_pk)
        form = UpdatePuntoResolucionForm(request.POST, instance=punto)
        if form.is_valid():
            form.save()
            return redirect('reunion_detail', pk=reunion_pk)
        return render(request, 'main/punto_update.html', {'form': form, 'tipo': "resolucion"})


class PuntoUpdateSeguimientoView(View):

    def get(self, request, punto_pk, reunion_pk):
        punto = Punto.objects.get(pk=punto_pk)
        form = UpdatePuntoSeguimientoForm(instance=punto)
        context = {
            'form': form,
            'tipo': "seguimiento"
        }
        return render(request, 'main/punto_update.html', context)

    def post(self, request, punto_pk, reunion_pk):
        punto = Punto.objects.get(pk=punto_pk)
        form = UpdatePuntoSeguimientoForm(request.POST, instance=punto)
        if form.is_valid():
            form.save()
            return redirect('reunion_detail', pk=reunion_pk)
        return render(request, 'main/punto_update.html', {'form': form, 'tipo': "seguimiento"})


class PuntoUpdateAdminView(View):

    def get_object(self, queryset=None, pk=None):
        obj = Punto.objects.get(id=self.kwargs['pk'])
        if obj.estado_punto == 'ST':
            return obj
        else:
            return None

    def get(self, request, pk):
        dni = username_to_dni(request.user.username)
        punto = self.get_object(Punto, pk=pk)
        form = UpdateAdminPuntoForm(instance=punto, org=organos_miembro(dni))
        context = {
            'form': form
        }
        return render(request, 'main/punto_update.html', context)

    def post(self, request, pk):
        punto = self.get_object(Punto, pk=pk)
        dni = username_to_dni(request.user.username)
        form = UpdateAdminPuntoForm(request.POST, instance=punto, org=organos_miembro(dni))
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('punto_consensuado', kwargs={'pk': punto.pk}))
        return render(request, 'main/punto_update.html', {'form': form})


class PuntoDeleteView(DeleteView):
    model = Punto
    success_url = reverse_lazy('puntos_list')
    template_name = "main/punto_delete.html"

    def get_object(self, queryset=None):
        obj = Punto.objects.get(id=self.kwargs['pk'])
        if obj.estado_punto == 'ST':
            return obj
        else:
            return None


class PuntosQuerySet(object):
    @staticmethod
    def get_punto_queryset(request):
        dni = username_to_dni(request.user.username)
        organo = request.session.get('organo')
        # si el usuario no tiene privilegios solo ve las suyas
        if miembro_tiene_privilegios(dni, organo) is False:
            puntos = Punto.objects.filter(Q(creador=request.user) & Q(organo=organo)).order_by('-fecha_modificacion')
        # si el usuario tiene privilegios
        else:
            puntos = Punto.objects.filter(organo=organo).order_by('-fecha_modificacion')
        return puntos


class PuntoListView(View, PuntosQuerySet):
    def get(self, request):
        """
            Devuelve:
            -Las propuestas de puntos creadas por el usuario para el organo elegido si éste no tiene privilegios
            -Todas las propuestas de puntos de ése órgano si éste tiene privilegios
            """
        dni = username_to_dni(request.user.username)
        organo = request.session.get('organo')
        context = {
            'puntos': self.get_punto_queryset(request),
            'usuario_tiene_permiso': miembro_tiene_privilegios(dni, organo)
        }
        return render(request, 'main/punto_list.html', context)


# Vistas de Reunion
class ReunionCreateView(View):

    def get(self, request):

        OrdenFormSet = modelformset_factory(Orden, form=OrdenForm, extra=1)
        organo = request.session.get('organo')
        form = CreateReunionForm()

        formset = OrdenFormSet(queryset=Orden.objects.none(), form_kwargs={'organo': organo})
        context = {
            'form': form,
            'formset': formset
        }
        return render(request, 'main/create_reunion.html', context)

    def post(self, request):
        OrdenFormSet = modelformset_factory(Orden, form=OrdenForm, extra=1)
        form = CreateReunionForm(request.POST)
        organo = request.session.get('organo')
        formset = OrdenFormSet(request.POST, queryset=Orden.objects.none(), form_kwargs={'organo': organo})
        if self.hay_puntos_repetidos(formset):
            return render(request, 'main/create_reunion.html', {'form': form, 'formset': formset,
                                                                'error': 'Por favor, seleccione cada propuesta una única vez'})
        if form.is_valid() and formset.is_valid():
            reunion = form.save(commit=False)
            reunion.creador = self.request.user
            reunion.organo = self.request.session.get('organo')
            reunion.duracion_estimada = timedelta(minutes=0)
            reunion.save()
            for count, form in enumerate(formset.cleaned_data):
                if form.get('punto') is not None:
                    punto = form.get('punto')
                    reunion.save()
                    orden = Orden(punto=punto, reunion=reunion, orden=count+1)
                    orden.save()

            ordenes = Orden.objects.filter(reunion=reunion)
            for orden in ordenes:
                reunion.duracion_estimada += orden.punto.duracion_estimada
            reunion.save()
            for orden in ordenes:
                orden.punto.estado_punto_anterior = orden.punto.estado_punto
                orden.punto.estado_punto = 'ADD'
                orden.punto.save()
            return redirect(reverse_lazy('reuniones_list'))
        return render(request, 'main/create_reunion.html', {'form': form, 'formset': formset})

    def hay_puntos_repetidos(self, formset):
        puntos = []
        for count, form in enumerate(formset.cleaned_data):
            puntos.append(form.get('punto'))
        if len(set(puntos)) == len(puntos):
            return False
        else:
            return True


class ReunionAsistentesView(View):

    def get(self, request, pk):
        reload(sys)
        sys.setdefaultencoding('UTF8')
        reunion = Reunion.objects.get(pk=pk)
        if request.GET.get('add'):
            self.add_asistente(request.GET.get('miembro'), reunion)
            request.GET.get == ""
            return redirect(reverse_lazy('reunion_asistentes', kwargs={'pk': reunion.pk}))
        if request.GET.get('delete'):
            self.delete_asistente(request.GET.get('miembro2'), reunion)
            request.GET.get == ""
            return redirect(reverse_lazy('reunion_asistentes', kwargs={'pk': reunion.pk}))
        context = {
            'miembros': lista_miembros_organo(self.request.session.get('organo')),
            'reunion': reunion,
        }
        return render(request, 'main/reunion_asistentes.html', context)

    def add_asistente(self, miembro, reunion):
        if reunion.asistentes is None:
            aux = []
        else:
            aux = str(reunion.asistentes).split(", ")
        aux.append(miembro)
        reunion.asistentes = ", ".join(aux)
        reunion.save()

    def delete_asistente(self, miembro, reunion):
        aux = str(reunion.asistentes).split(", ")
        aux.remove(miembro)
        reunion.asistentes = ", ".join(aux)
        reunion.save()


class ReunionListView(View):

    def get(self, request):
        """
            Devuelve las reuniones del órgano seleccionado
            """
        dni = username_to_dni(request.user.username)
        organo = request.session.get('organo')
        context = {
            'reuniones': Reunion.objects.filter(organo=request.session.get('organo')).order_by('-fecha_hora'),
            'usuario_tiene_permiso': miembro_tiene_privilegios(dni, organo)
        }
        return render(request, 'main/reunion_list.html', context)


class ReunionDetailView(DetailView):
    model = Reunion
    template_name = "main/reunion_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ReunionDetailView, self).get_context_data(**kwargs)
        ordenes = Orden.objects.filter(reunion=self.get_object())
        list_puntos = []
        for orden in ordenes:
            list_puntos.append(orden.punto)
        context['puntos'] = list_puntos
        return context

    def usuario_tiene_permiso(self):
        dni = username_to_dni(self.request.user.username)
        organo = self.request.session.get('organo')
        return miembro_tiene_privilegios(dni, organo)


# class ReunionUpdateView(View):
#
#     def get_object(self, queryset=None, pk=None):
#         obj = Reunion.objects.get(id=self.kwargs['pk'])
#         if obj.estado_reunion != 'CELE':
#             return obj
#         else:
#             return None
#
#     def get(self, request, pk):
#         OrdenFormSet = modelformset_factory(Orden, form=OrdenForm, can_delete=True, extra=1)
#         dni = username_to_dni(request.user.username, )
#         reunion = self.get_object(Reunion, pk=pk)
#         organo = request.session.get('organo')
#         form = UpdateReunionForm(instance=reunion, org=organos_miembro(dni))
#         queryset = Orden.objects.filter(reunion=reunion)
#         formset = OrdenFormSet(queryset=queryset, form_kwargs={'organo': organo})
#         context = {
#             'form': form,
#             'reunion': reunion,
#             'formset': formset
#         }
#         return render(request, 'main/reunion_update.html', context)
#
#     def post(self, request, pk):
#         OrdenFormSet = modelformset_factory(Orden, form=OrdenForm, can_delete=True, extra=1)
#         reunion = self.get_object(Reunion, pk=pk)
#         queryset = Orden.objects.filter(reunion=reunion)
#         dni = username_to_dni(request.user.username)
#         organo = request.session.get('organo')
#         form = UpdateReunionForm(request.POST, instance=reunion, org=organos_miembro(dni))
#         formset = OrdenFormSet(request.POST, queryset=queryset, form_kwargs={'organo': organo})
#         instances = formset.save(commit=False)
#         if form.is_valid() and formset.is_valid():
#             reunion.duracion_estimada = timedelta(minutes=0)
#             reunion = form.save()
#             if formset.deleted_objects:
#                 for obj in formset.deleted_objects:
#                     print(obj)
#                     os.unlink(obj.documento.path)
#                     try:
#                         dirind = obj.documento.path.rfinf('/')
#                         dir = obj.fichero.path[:dirind]
#                         os.removedirs(dir)
#                     except:
#                         pass
#                     # ordenes = Orden.objects.filter(reunion=reunion)
#                     # for orden in ordenes:
#                     #     orden.punto.estado_punto, orden.punto.estado_punto_anterior = orden.punto.estado_punto_anterior, orden.punto.estado_punto
#                     #     orden.punto.save()
#                     obj.delete()
#             for count, form in enumerate(formset.cleaned_data):
#                 if form.get('punto') is not None:
#                     punto = form.get('punto')
#                     reunion.save()
#                     orden = Orden(punto=punto, reunion=reunion, orden=count+1)
#                     orden.save()
#             for punto in reunion.puntos.all():
#                 reunion.duracion_estimada += punto.duracion_estimada
#             reunion.save()
#
#             return redirect('reuniones_list')

class ReunionDeleteView(DeleteView):
    model = Reunion
    success_url = reverse_lazy('reuniones_list')
    template_name = "main/reunion_delete.html"

    def get_object(self, queryset=None, pk=None):
        obj = Reunion.objects.get(id=self.kwargs['pk'])
        if obj.estado_reunion == 'CRE':
            return obj
        else:
            return None

    def delete(self, request, *args, **kwargs):
        reunion = self.get_object(Reunion, pk=self.kwargs['pk'])
        ordenes = Orden.objects.filter(reunion=reunion)
        for orden in ordenes:
            if orden.punto.estado_punto_anterior:
                orden.punto.estado_punto = orden.punto.estado_punto_anterior
            else:
                orden.punto.estado_punto = 'ST'
            orden.punto.save()
        reunion.delete()
        return redirect('reuniones_list')

class ConvocarReunionView(View):
    def get_object(self, queryset=None, pk=None):
        obj = Reunion.objects.get(id=self.kwargs['pk'])
        if obj.estado_reunion == 'CRE':
            return obj
        else:
            return None

    def get(self, request, pk):
        reunion = self.get_object(Reunion, pk=self.kwargs['pk'])
        reunion.estado_reunion = 'CONV'
        reunion.save()
        ordenes = Orden.objects.filter(reunion=reunion)
        puntos = ''
        for orden in ordenes:
            orden.punto.estado_punto_anterior = orden.punto.estado_punto
            orden.punto.estado_punto = 'CONV'
            orden.punto.save()
            puntos = puntos + '- ' + orden.punto.nombre_admin+'.\n'

        destinatarios = lista_miembros_organo_email(self.request.session.get('organo'))
        #print(destinatarios)
        Organo = self.request.session.get('organo')

        Asunto = 'Convocada Reunion del '+Organo+'.'
        Texto = 'Estimado miembro del '+Organo+',\n\n' \
                                               'Se ha convocado una Reunion para la fecha: \n'\
                +unicode(_date(reunion.fecha_hora, 'l d F Y H:i'))+\
                '\nen '+reunion.lugar+', en la que se trataran los siguientes puntos del dia: \n'+puntos+\
                '\nEsperamos su asistencia.\n\nReciba un cordial saludo y muchas gracias.\n\n\nMensaje generado automaticamente, por favor, no lo responda.'
        email = EmailMessage(Asunto, Texto, to=['amandaoliversanchez@gmail.com'])
        email.send()

        return HttpResponseRedirect(reverse_lazy('reunion_detail', args=[pk]))


class DesconvocarReunionView(View):
    def get_object(self, queryset=None, pk=None):
        obj = Reunion.objects.get(id=self.kwargs['pk'])
        if obj.estado_reunion == 'CONV':
            return obj
        else:
            return None

    def get(self, request, pk):
        reunion = self.get_object(Reunion, pk=self.kwargs['pk'])
        reunion.estado_reunion = 'CRE'
        reunion.save()
        ordenes = Orden.objects.filter(reunion=reunion)
        for orden in ordenes:
            if orden.punto.estado_punto_anterior:
                orden.punto.estado_punto = orden.punto.estado_punto_anterior
            else:
                orden.punto.estado_punto = 'ADD'
            orden.punto.save()
        destinatarios = lista_miembros_organo_email(self.request.session.get('organo'))
        # print(destinatarios)
        Organo = self.request.session.get('organo')

        Asunto = 'Desconvocada Reunion del ' + Organo + '.'
        Texto = 'Estimado miembro del ' + Organo + ',\n\n' \
                                                   'Se ha desconvocado la Reunion de la fecha: \n' \
                + unicode(_date(reunion.fecha_hora, 'l d F Y H:i')) + \
                '\nen ' + reunion.lugar + '.\nPor favor, elimine la cita de su agenda, sentimos mucho los inconvenientes ocasionados.' \
                                          '\n\nReciba un cordial saludo y muchas gracias.\n\n\nMensaje generado automaticamente, por favor, no lo responda.'
        email = EmailMessage(Asunto, Texto, to=['amandaoliversanchez@gmail.com'])
        email.send()
        return HttpResponseRedirect(reverse_lazy('reunion_detail', args=[pk]))


class CerrarActaView(View):
    def get_object(self, queryset=None, pk=None):
        obj = Reunion.objects.get(id=self.kwargs['pk'])
        if obj.estado_reunion == 'CONV':
            return obj
        else:
            return None

    # Cambiar estado de los puntos tratados
    def get(self, request, pk):
        reunion = self.get_object(Reunion, pk=self.kwargs['pk'])
        reunion.estado_reunion = 'CELE'
        reunion.save()
        return HttpResponseRedirect(reverse_lazy('reunion_detail', args=[pk]))




