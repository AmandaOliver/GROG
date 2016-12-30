# coding: utf-8

import ldap
from django_auth_ldap.config import LDAPSearch, PosixGroupType

# Configuración de backends de Django
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_auth_ldap.backend.LDAPBackend',
)

# Configuración de la conexión cifrada
AUTH_LDAP_START_TLS = True
AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: False,
    ldap.OPT_REFERRALS: False,
}

# Configuración base del LDAP
AUTH_LDAP_SERVER_URI = "ldap://ldap.uca.es"
AUTH_LDAP_BIND_DN = "cn=anonimo,dc=uca,dc=es"
AUTH_LDAP_BIND_PASSWORD = "anonimo"

# Búsqueda de usuarios
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "dc=uca,dc=es",
    ldap.SCOPE_SUBTREE,
    "(uid=%(user)s)"
)

# Búsqueda de grupos
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    "dc=uca,dc=es",
    ldap.SCOPE_SUBTREE,
    "(objectClass=posixGroup)"
)

# Tipo de grupo por defecto
AUTH_LDAP_GROUP_TYPE = PosixGroupType()

# Mapeo de parámetros entre usuarios de LDAP y usuarios del modelo User
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}

# Actualizar el usuario siempre con los datos del LDAP
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Copiar los grupos del LDAP a grupos de Django
AUTH_LDAP_MIRROR_GROUPS = False

# Copiar los permisos de grupo de LDAP según los grupos de Django
AUTH_LDAP_FIND_GROUP_PERMS = False

# Cacheo
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 2
