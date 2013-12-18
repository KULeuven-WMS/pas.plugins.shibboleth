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

from Products.CMFCore.utils import getToolByName
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
        """ get the unit information from REQUEST upon login
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
            groups = request.environ.get('HTTP_KULOUNUMBER')
            if groups:
                groups = groups.split(';')
                groups.extend(self.getAffiliations(request, groups))
            else:
                groups = []
        else:
            return ()
        groups = tuple(groups)
        self.ZCacheable_set(groups, view_name)
        return groups

    def getAffiliations(self, request, groups):
        """ get affiliation information from REQUEST upon login """
        raw_affiliations = request.environ.get('HTTP_AFFILIATION')
        if not raw_affiliations:
            return []
        raw_affiliations = raw_affiliations.split(';')
        affiliations = [af[:af.find('@')].upper() for af in raw_affiliations
                        if af in ('staff@kuleuven.be',
                                  'zap@kuleuven.be',
                                  'bap@kuleuven.be',
                                  'aap@kuleuven.be',
                                  'op3@kuleuven.be',
                                  'affiliate@kuleuven.be')
                        ]
        result = []
        import itertools
        for group, affiliation in itertools.product(groups, affiliations):
            # map affiliations with their display names
            if 'STAFF' in affiliation:
                affiliation = 'ATP'
            if 'AFFILIATE' in affiliation:
                affiliation = 'Affiliate'
            result.append("%s|%s" % (group, affiliation))
        return result

    #
    # IGroupsIntrospection implementation for business groups
    #
    security.declarePrivate('getGroupById')

    def getGroupById(self, group_id):
        """ for virtual groups formed as unit number plus affiliation
        """
        if not group_id:
            return None

        import re
        if re.match("\w+\|\w+", group_id):
            unit_nr, unit_affiliation = group_id.split('|')
            gtool = getToolByName(self, 'portal_groups')
            unit = gtool.getGroupById(unit_nr)
            unit_title = unit_nr
            if unit:
                unit_title = unit.getProperty('title')
            virt_group_title = "%s (%s)" % (unit_title, unit_affiliation)
            return VirtualGroup(group_id, title=virt_group_title, \
                                description=virt_group_title)

    def getGroupMembers(self, group_id):
        """ skip for virtual groups formed as unit number plus affiliations
        """
        return []


classImplements(ShibGroupManager,
                IGroupsPlugin,
                IGroupIntrospection)

InitializeClass(ShibGroupManager)
