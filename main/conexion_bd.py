# -*- coding: utf-8 -*-

import psycopg2

consulta_organos_miembro = """SELECT DISTINCT
  grupos_modelos_funcion.nombre,
  grupos_modelos_organo.nombre,
  grupos_modelos_miembro.dni,
  grupos_modelos_miembro.nombre,
  grupos_modelos_miembro.apellido1,
  grupos_modelos_miembro.apellido2
FROM
  public.grupos_modelos_miembro,
  public.grupos_modelos_funcion,
  public.grupos_modelos_organo,
  public.grupos_modelos_grupo,
  public.grupos_modelos_asignaciongrupo,
  public.grupos_modelos_asignacionfuncion
WHERE
  grupos_modelos_asignaciongrupo.miembro_id = grupos_modelos_miembro.id AND
  grupos_modelos_asignaciongrupo.grupo_id = grupos_modelos_grupo.id AND
  grupos_modelos_asignacionfuncion.organo_id = grupos_modelos_organo.id AND
  grupos_modelos_asignacionfuncion.funcion_id = grupos_modelos_funcion.id AND
  grupos_modelos_asignacionfuncion.grupo_id = grupos_modelos_grupo.id AND
  (grupos_modelos_asignaciongrupo.desde IS NULL OR grupos_modelos_asignaciongrupo.desde <= CURRENT_DATE) AND
  (grupos_modelos_asignaciongrupo.hasta IS NULL OR grupos_modelos_asignaciongrupo.hasta >= CURRENT_DATE) AND
  grupos_modelos_miembro.dni = '{0}'
ORDER BY
  grupos_modelos_miembro.dni ASC;
"""

consulta_miembro_tiene_privilegios = """SELECT
  grupos_modelos_organo.nombre,
  grupos_modelos_funcion.nombre,
  grupos_modelos_miembro.nombre,
  grupos_modelos_miembro.apellido1,
  grupos_modelos_miembro.dni
FROM
  public.grupos_modelos_asignacionfuncion,
  public.grupos_modelos_asignaciongrupo,
  public.grupos_modelos_funcion,
  public.grupos_modelos_miembro,
  public.grupos_modelos_organo
WHERE
  grupos_modelos_asignacionfuncion.grupo_id = grupos_modelos_asignaciongrupo.grupo_id AND
  grupos_modelos_asignacionfuncion.funcion_id = grupos_modelos_funcion.id AND
  grupos_modelos_asignacionfuncion.organo_id = grupos_modelos_organo.id AND
  grupos_modelos_asignaciongrupo.miembro_id = grupos_modelos_miembro.id AND
  grupos_modelos_miembro.dni = '{0}' AND
  grupos_modelos_organo.nombre = '{1}' AND
  (grupos_modelos_funcion.nombre = 'Secretario' OR grupos_modelos_funcion.nombre = 'Presidente')
ORDER BY
  grupos_modelos_miembro.nombre ASC;

"""
consulta_lista_miembros_organo = """SELECT DISTINCT
  grupos_modelos_organo.nombre,
  grupos_modelos_funcion.nombre,
  grupos_modelos_miembro.nombre,
  grupos_modelos_miembro.apellido1,
  grupos_modelos_miembro.apellido2,
  grupos_modelos_miembro.dni
FROM
  public.grupos_modelos_asignacionfuncion,
  public.grupos_modelos_asignaciongrupo,
  public.grupos_modelos_funcion,
  public.grupos_modelos_miembro,
  public.grupos_modelos_organo
WHERE
  grupos_modelos_asignacionfuncion.grupo_id = grupos_modelos_asignaciongrupo.grupo_id AND
  grupos_modelos_asignacionfuncion.funcion_id = grupos_modelos_funcion.id AND
  grupos_modelos_asignacionfuncion.organo_id = grupos_modelos_organo.id AND
  grupos_modelos_asignaciongrupo.miembro_id = grupos_modelos_miembro.id AND
  grupos_modelos_organo.nombre = '{0}'
ORDER BY
  grupos_modelos_miembro.nombre ASC;"""

consulta_lista_miembros_organo_email = """SELECT DISTINCT grupos_modelos_email.email
FROM
  public.grupos_modelos_asignacionfuncion,
  public.grupos_modelos_asignaciongrupo,
  public.grupos_modelos_funcion,
  public.grupos_modelos_miembro,
  public.grupos_modelos_organo,
  public.grupos_modelos_email
WHERE
  grupos_modelos_asignacionfuncion.grupo_id = grupos_modelos_asignaciongrupo.grupo_id AND
  grupos_modelos_asignacionfuncion.funcion_id = grupos_modelos_funcion.id AND
  grupos_modelos_asignacionfuncion.organo_id = grupos_modelos_organo.id AND
  grupos_modelos_asignaciongrupo.miembro_id = grupos_modelos_miembro.id AND
  grupos_modelos_email.usuario_id = grupos_modelos_miembro.id AND
  grupos_modelos_organo.nombre = '{0}';"""

def organos_miembro(dni, dict_consulta=None):
    connection = psycopg2.connect(database='goc_django', user='goclectura', password='znHiRA',
                                  host='virtualmindj.uca.es', client_encoding='utf-8')
    valor_atributo = []
    try:
        cursor = connection.cursor()
        if dict_consulta is None:
            cursor.execute(consulta_organos_miembro.format(dni))
        else:
            cursor.execute(consulta_organos_miembro, dict_consulta)
        rows = cursor.fetchall()
        for row in rows:
            valor_atributo.append(row[1])
    finally:
        connection.close()

    if valor_atributo is None or valor_atributo == '':
        valor_atributo = (None, )
    return valor_atributo


def miembro_tiene_privilegios(dni, organo, dict_consulta=None):
    connection = psycopg2.connect(database='goc_django', user='goclectura', password='znHiRA',
                                  host='virtualmindj.uca.es', client_encoding='utf-8')
    valor_atributo = []
    try:
        cursor = connection.cursor()
        if dict_consulta is None:
            cursor.execute(consulta_miembro_tiene_privilegios.format(dni, organo))
        else:
            cursor.execute(consulta_miembro_tiene_privilegios, dict_consulta)
        rows = cursor.fetchall()
        for row in rows:
            valor_atributo.append(row[1])
    finally:
        connection.close()
    if valor_atributo is None or valor_atributo == []:
        return False
    else:
        return True


def lista_miembros_organo(organo, dict_consulta=None):
    connection = psycopg2.connect(database='goc_django', user='goclectura', password='znHiRA',
                                  host='virtualmindj.uca.es', client_encoding='utf-8')
    valor_atributo = []
    try:
        cursor = connection.cursor()
        if dict_consulta is None:
            cursor.execute(consulta_lista_miembros_organo.format(organo))
        else:
            cursor.execute(consulta_lista_miembros_organo, dict_consulta)
        rows = cursor.fetchall()
        for row in rows:
            miembro = row[2]+" "+row[3]+" "+row[4]
            valor_atributo.append(miembro)

    finally:
        connection.close()

    if valor_atributo is None or valor_atributo == '':
        valor_atributo = (None,)
    return valor_atributo

def lista_miembros_organo_email(organo, dict_consulta=None):
    connection = psycopg2.connect(database='goc_django', user='goclectura', password='znHiRA',
                                  host='virtualmindj.uca.es', client_encoding='utf-8')
    valor_atributo = []
    try:
        cursor = connection.cursor()
        if dict_consulta is None:
            cursor.execute(consulta_lista_miembros_organo_email.format(organo))
        else:
            cursor.execute(consulta_lista_miembros_organo_email, dict_consulta)
        rows = cursor.fetchall()
        for row in rows:
            miembro = row[0]
            valor_atributo.append(miembro)

    finally:
        connection.close()

    if valor_atributo is None or valor_atributo == '':
        valor_atributo = (None,)
    return valor_atributo