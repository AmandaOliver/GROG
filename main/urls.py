# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from main.views import HomeView, PuntoCreateView, ReunionCreateView, PuntoListView, ReunionListView, \
    PuntoUpdateView, PuntoDetailView, ReunionDetailView, PuntoDeleteView, SeleccionOrganoView, \
    ReunionDeleteView, PuntoUpdateAdminView, ConvocarReunionView, CerrarActaView, PuntoUpdateResolucionView, \
    DesconvocarReunionView, PuntoConsensuadoView, ReunionAsistentesView, PuntoUpdateSeguimientoView

urlpatterns = [

    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),

    # Organos URLs
    url(r'^seleccion/organo', login_required(SeleccionOrganoView.as_view()), name="seleccion_organo"),

    # Puntos URLs
    url(r'^punto/create', login_required(PuntoCreateView.as_view()), name="create_punto"),
    url(r'^punto/(?P<pk>[0-9]+)$', login_required(PuntoDetailView.as_view()), name="punto_detail"),
    url(r'^punto/consensuado_con/(?P<pk>[0-9]+)$', login_required(PuntoConsensuadoView.as_view()), name="punto_consensuado"),
    url(r'^puntos/list', login_required(PuntoListView.as_view()), name="puntos_list"),
    url(r'^punto/update/(?P<pk>[0-9]+)$', login_required(PuntoUpdateView.as_view()), name="punto_update"),
    url(r'^punto/update/admin/(?P<pk>[0-9]+)$', login_required(PuntoUpdateAdminView.as_view()), name="punto_update_admin"),
    url(r'^punto/update/resolucion/(?P<punto_pk>[0-9]+)/(?P<reunion_pk>[0-9]+)$',
        login_required(PuntoUpdateResolucionView.as_view()), name="punto_update_resolucion"),
    url(r'^punto/update/seguimiento/(?P<punto_pk>[0-9]+)/(?P<reunion_pk>[0-9]+)$',
        login_required(PuntoUpdateSeguimientoView.as_view()), name="punto_update_seguimiento"),
    url(r'^punto/delete/(?P<pk>[0-9]+)$', login_required(PuntoDeleteView.as_view()), name="punto_delete"),


    # Reuniones URLs
    url(r'^reunion/create', login_required(ReunionCreateView.as_view()), name="create_reunion"),
    url(r'^reuniones/list', login_required(ReunionListView.as_view()), name="reuniones_list"),
    url(r'^reunion/(?P<pk>[0-9]+)$', login_required(ReunionDetailView.as_view()), name="reunion_detail"),
    url(r'^reunion/asistentes/(?P<pk>[0-9]+)$', login_required(ReunionAsistentesView.as_view()), name="reunion_asistentes"),
    # url(r'^reunion/update/(?P<pk>[0-9]+)$', login_required(ReunionUpdateView.as_view()), name="reunion_update"),
    url(r'^reunion/delete/(?P<pk>[0-9]+)$', login_required(ReunionDeleteView.as_view()), name="reunion_delete"),
    url(r'^reunion/convocar/(?P<pk>[0-9]+)$', login_required(ConvocarReunionView.as_view()), name="convocar_reunion"),
    url(r'^reunion/desconvocar/(?P<pk>[0-9]+)$', login_required(DesconvocarReunionView.as_view()), name="desconvocar_reunion"),
    url(r'^reunion/cerrar/(?P<pk>[0-9]+)$', login_required(CerrarActaView.as_view()), name="cerrar_acta"),

]