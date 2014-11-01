# -*- coding: utf-8 -*-
"""
pas.plugins.shibboleth

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by KULeuven

$Id: event.py 67630 2006-04-27 00:54:03Z peterjacobs $
"""
from OFS.Cache import Cacheable
from AccessControl import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass

from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin  # NOQA
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
import logging

manage_addShibUserEnumerationManagerForm = \
    PageTemplateFile('www/ShibUserEnumerationManagerForm',
                     globals())


def manage_addShibUserEnumerationManager(self, id, title='', REQUEST=None):
    """Add a user enumeration plugin to a Pluggable Auth Service.
    """
    rm = ShibUserEnumerationManager(id, title)
    self._setObject(rm.getId(), rm)
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
            '%s/manage_workspace'
            '?manage_tabs_message='
            'SAGroupManager+added.' % self.absolute_url())

logger = logging.getLogger('pas.plugins.shibboleth')


class ShibUserEnumerationManager(BasePlugin, Cacheable):
    """
    A user enumeration manager plugin for shibboleth
    """

    security = ClassSecurityInfo()
    meta_type = 'ShibUserEnumerationManager'
    manage_options = tuple(BasePlugin.manage_options +
                           Cacheable.manage_options)

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

    #
    #   IUserEnumerationPlugin implementation
    #
    security.declarePrivate('enumerateUsers')

    def enumerateUsers(self, id=None, login=None, exact_match=False,
                       sort_by=None, max_results=None, **kw):
        if login is None and id is not None:
            login = id
        if login is not None and exact_match and \
           hasattr(self, 'REQUEST') and \
           login == self.REQUEST.environ.get('HTTP_EPPN'):
            return ({'id': login,
                     'login': login,
                     'pluginid': self.getId()}, )
        return ()

classImplements(ShibUserEnumerationManager,
                IUserEnumerationPlugin)

InitializeClass(ShibUserEnumerationManager)
