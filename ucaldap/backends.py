# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django_auth_ldap.backend import LDAPBackend
from django_auth_ldap.config import _LDAPConfig

logger = _LDAPConfig.get_logger()


class NoCreateLDAPBackend(LDAPBackend):
    """
    Especialización del LDAPBackend de django_auth_ldap que no crea
    usuarios nuevos, sino que exige que ya estén registrados en el
    sistema.

    Para usarlo, usar 'ucaldap.backends.NoCreateLDAPBackend' en el
    ajuste AUTHENTICATION_BACKENDS del settings.py
    """

    def authenticate(self, username, password):
        if not User.objects.filter(username=username).count():
            logger.debug('User %s does not exist ' % username)
            return None
        return super(NoCreateLDAPBackend, self).authenticate(username, password)
