# -*- coding: utf-8 -*-
"""
pas.plugins.shibboleth

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
from zope.interface import Interface


class IShibUserPropertiesManager(Interface):
    """
    Shibboleth user properties manager marker interface
    """


class IShibRoleManager(Interface):
    """
    Shibboleth user role manager marker interface
    """


class IUserPropertyFilter(Interface):
    """
    Filter user properties content
    """
