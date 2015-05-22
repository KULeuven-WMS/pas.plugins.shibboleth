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
from Products.PlonePAS.interfaces.group import IGroupIntrospection
from Products.PlonePAS.plugins.autogroup import VirtualGroup
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
        REQUEST['RESPONSE'].redirect('%s/manage_workspace'
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
    manage_options = tuple(BasePlugin.manage_options +
                           Cacheable.manage_options)

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

    #
    # IGroupsPlugin implementation
    #
    security.declarePrivate('getGroupsForPrincipal')

    def getGroupsForPrincipal(self, principal, request=None):
        """ get the groups information from REQUEST upon login
        """
        if request is None:
            if hasattr(self, 'REQUEST'):
                request = self.REQUEST
            else:
                return []
        view_name = createViewName('getGroupsForPrincipal',
                                   principal.getId())
        cached_info = self.ZCacheable_get(view_name)
        if cached_info is not None:
            return cached_info
        groups = []
        authUser = request.environ.get('HTTP_EPPN')
        if authUser and authUser == principal.getId():
            units = request.environ.get('HTTP_KULOUNUMBER')
            if units:
                groups = units.split(';')
            groups.extend(self.getAffiliations(request, groups))
        else:
            return ()
        groups = tuple(groups)
        self.ZCacheable_set(groups, view_name)
        return groups

    def getAffiliations(self, request, units=[]):
        """ fetch and keep affiliations from REQUEST upon login """

        unscoped_affiliations = request.environ.get(
            'HTTP_UNSCOPED_AFFILIATION')
        if not unscoped_affiliations:
            return []

        affiliations = unscoped_affiliations.split(';')
        scoped_affiliations = request.environ.get('HTTP_AFFILIATION')
        if scoped_affiliations:
            affiliations.extend(scoped_affiliations.split(';'))

            if not units:
                return affiliations

            # @kuleuven: units combined with different employee affiliations
            kul_affiliations = [aff[:aff.find('@')] for aff in affiliations
                                if aff in ('staff@kuleuven.be',
                                           'zap@kuleuven.be',
                                           'bap@kuleuven.be',
                                           'aap@kuleuven.be',
                                           'op3@kuleuven.be')]
            if kul_affiliations:
                import itertools
                for unit, affiliation in itertools.product(units,
                                                           kul_affiliations):
                    affiliations.append("%s|%s" % (unit, affiliation))
        return affiliations

    #
    # IGroupsIntrospection implementation for business groups
    #
    security.declarePrivate('getGroupById')

    def getGroupById(self, group_id):
        """ for groups with unit|affiliation
        """
        if not group_id:
            return None

        import re
        if re.match("\w+\|\w+", group_id):
            return VirtualGroup(group_id, title=group_id)

    def getGroupMembers(self, group_id):
        """ skip for groups with unit|affiliation
        """
        return []

    def getGroups(self):
        """ skip for groups with unit|affiliation
        """
        return []

    def getGroupIds(self):
        """ skip for groups with unit|affiliation
        """
        return []


classImplements(ShibGroupManager,
                IGroupsPlugin,
                IGroupIntrospection)

InitializeClass(ShibGroupManager)
