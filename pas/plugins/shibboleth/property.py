# -*- coding: utf-8 -*-
"""
pas.plugins.shibboleth

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
import logging
from AccessControl import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.UserPropertySheet import UserPropertySheet

manage_addShibUserPropertiesManagerForm = PageTemplateFile('www/ShibGroupManagerForm',
                                               globals())


def manage_addShibUserProperties(self, id, title='',
                            REQUEST=None):
    """Add a  to a Pluggable Auth Service.
    """
    rm = ShibUserPropertiesManager(id, title)
    self._setObject(rm.getId(), rm)
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
                                '%s/manage_workspace'
                                '?manage_tabs_message='
                                'ShibUserPropertiesManager+added.'
                            % self.absolute_url())

logger = logging.getLogger('pas.plugins.shibboleth')


class ShibUserPropertiesManager(BasePlugin):
    """
    An user properties manager plugin for shibboleth
    """
    security = ClassSecurityInfo()
    meta_type = 'ShibGroupManager'
    manage_options = tuple(BasePlugin.manage_options)
    user_properties_mapping = {'HTTP_KULMAIL': 'mail',
                               'HTTP_KULFULLNAME': 'fullname'}

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

    def _getShibProperties(self):
        userProperties = {}
        for requestId, propertyId in self.user_properties_mapping.items():
            requestValue = self.REQUEST.environ.get(requestId)
            if requestValue is not None:
                userProperties[propertyId] = requestValue
        return userProperties
    #
    # IPropertiesPlugin implementation
    #
    def getPropertiesForUser(self, user, request=None):
        """ user -> {}

        o User will implement IPropertiedUser.

        o Plugin should return a dictionary or an object providing
          IPropertySheet.

        o Plugin may scribble on the user, if needed (but must still
          return a mapping, even if empty).

        o May assign properties based on values in the REQUEST object, if
          present
        """
        return UserPropertySheet(user.id, **self._getShibProperties())

classImplements(ShibUserPropertiesManager,
                IPropertiesPlugin)


InitializeClass(ShibUserPropertiesManager)
