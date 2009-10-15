# -*- coding: utf-8 -*-
"""
pas.plugins.shibboleth

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
from OFS.Cache import Cacheable
from AccessControl import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass

from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import IGroupsPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import createViewName
import logging

manage_addShibGroupManagerForm = PageTemplateFile('www/ShibGroupManagerForm',
                                               globals())


def manage_addShibGroupManager(self, id, title='', REQUEST=None):
    """Add a GroupManager to a Pluggable Auth Service.
    """
    rm = ShibGroupManager(id, title)
    self._setObject(rm.getId(), rm)
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
                                '%s/manage_workspace'
                                '?manage_tabs_message='
                                'SAGroupManager+added.'
                            % self.absolute_url())

logger = logging.getLogger('pas.plugins.shibboleth')


class ShibGroupManager(BasePlugin, Cacheable):
    """
    A group manager plugin for shibboleth
    """

    security = ClassSecurityInfo()
    meta_type = 'ShibGroupManager'
    manage_options = tuple(BasePlugin.manage_options +\
                           Cacheable.manage_options)

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

    #
    # IGroupsPlugin implementation
    #
    security.declarePrivate('getGroupsForPrincipal')

    def getGroupsForPrincipal(self, principal, request=None):
        """ get the group information from the REQUEST
        """
        view_name = createViewName('getGroupsForPrincipal',
                                   principal.getId())
        cached_info = self.ZCacheable_get(view_name)
        if cached_info is not None:
            return cached_info
        groups = []
        authUser = self.REQUEST.environ.get('HTTP_EPPN')
        if authUser and authUser == principal.getId():
            #groups = self.REQUEST.get('HTTP_KULPRIMONUMBER')
            groups = self.REQUEST.environ.get('HTTP_KULOUNUMBER')
            if groups:
                groups = groups.split(';')
            else:
                groups = []
        else:
            return ()
        groups = tuple(groups)
        self.ZCacheable_set(groups, view_name)
        return groups

classImplements(ShibGroupManager,
                IGroupsPlugin)

InitializeClass(ShibGroupManager)
