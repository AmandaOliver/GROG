# -*- coding: utf-8 -*-

# Tipos de puntos
INFORMACION = 'INFO'
APROBACION = 'APRO'
DELIBERACION_SIN_APROBACION = 'DSA'
DELIBERACION_CON_APROBACION = 'DCA'
TIPOS_PUNTOS = (
    (INFORMACION, "Información"),
    (APROBACION, "Aprobación por Consejo de Dirección"),
    (DELIBERACION_SIN_APROBACION, "Deliberación sin aprobación por Consejo de Dirección"),
    (DELIBERACION_CON_APROBACION, "Deliberación con aprobación por Consejo de Dirección"),
)

# Estado de los puntos
INFORMADO_POSITIVAMENTE = 'INPO'
APROBADO = 'ACD'
DELIBERADO = 'DEL'
SIN_TRATAR = 'ST'
TRASLADADO = 'TRAS'
RECHAZADO = 'RECH'
CONVOCADO = 'CONV'
ADDED = 'ADD'
ESTADO_PUNTOS = (
    (INFORMADO_POSITIVAMENTE, "Informado positivamente"),
    (APROBADO, "Aprobado por Consejo de Dirección"),
    (DELIBERADO, "Deliberado"),
    (SIN_TRATAR, "Sin tratar"),
    (TRASLADADO, "Trasladado a otra reunión"),
    (RECHAZADO, "Rechazado"),
    (CONVOCADO, "Convocado"),
    (ADDED, "Añadido a una reunión"),
)

# Estado de las reuniones
CREADA = 'CRE'
CONVOCADA = 'CONV'
CELEBRADA = 'CELE'
ESTADO_REUNIONES = (
    (CREADA, 'Creada'),
    (CONVOCADA, 'Convocada'),
    (CELEBRADA, 'Celebrada')
)
