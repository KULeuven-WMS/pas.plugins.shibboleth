# -*- coding: utf-8 -*-
"""
pas.plugins.shibboleth

Licensed under the GPL license, see LICENCE.txt for more details.

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
from AccessControl import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass

from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements

from pas.plugins.shibboleth.interfaces import IShibRoleManager

manage_addShibRoleManagerForm = PageTemplateFile('www/ShibRoleManagerForm',
                                               globals())


def manage_addShibRoleManager(self, id='shibrole', title='', REQUEST=None):
    """Add a  to a Pluggable Auth Service.
    """
    rm = ShibRoleManager(id, title)
    self._setObject(rm.getId(), rm)
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
                                '%s/manage_workspace'
                                '?manage_tabs_message='
                                'ShibRoleManager+added.'
                            % self.absolute_url())


class ShibRoleManager(BasePlugin):
    """
    A role manager plugin for shibboleth
    """


    security = ClassSecurityInfo()

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

    #
    # IRolesPlugin
    #
    security.declarePrivate('getRolesForPrincipal')

    def getRolesForPrincipal(self, user, request=None):
        """ Fullfill RolesPlugin requirements """
        if user.getId() == self.REQUEST.environ.get('HTTP_EPPN'):
            return ('Member', 'Anonymous')
        else:
            return ()

classImplements(ShibRoleManager,
                IShibRoleManager,
                IRolesPlugin)


InitializeClass(ShibRoleManager)
