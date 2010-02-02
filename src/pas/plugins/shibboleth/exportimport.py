# -*- coding: utf-8 -*-
"""
pas.plugins.shibboleth

Licensed under the GPL license, see LICENCE.txt for more details.
"""
import os

from Acquisition import aq_base

from zope.interface import implements
from zope.component import adapts

from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.interfaces import IFilesystemImporter
from Products.GenericSetup.interfaces import IFilesystemExporter
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import PropertyManagerHelpers
from Products.GenericSetup.utils import XMLAdapterBase

from pas.plugins.shibboleth.interfaces import IShibUserPropertiesManager
from pas.plugins.shibboleth.property import manage_addShibUserProperties


class ShibUserPropertiesExportImport(object):
    implements(IFilesystemExporter, IFilesystemImporter)

    def __init__(self, context):
        self.context = context

    def export(self, export_context, subdir, root=False):
        exportObjects(self.context, subdir + os.sep, export_context)

    def import_(self, import_context, subdir, root=False):
        importObjects(self.context, subdir + os.sep, import_context)

    def listExportableItems(self):
        return ()


class ShibPropertiesXMLAdapter(XMLAdapterBase, PropertyManagerHelpers):
    adapts(IShibUserPropertiesManager, ISetupEnviron)
    name = 'shibproperties'
    _LOGGER_ID = 'shibproperties'
    _encoding = 'utf-8'

    def _exportNode(self):
        node = self._doc.createElement('shibproperties')
        node.appendChild(self._extractProperties())
        self._logger.info('Site properties exported.')
        return node

    def _importNode(self, node):
        purge = self.environ.shouldPurge()
        if node.getAttribute('purge'):
            purge = self._convertToBoolean(node.getAttribute('purge'))
        if purge:
            self._purgeProperties()
        self._initProperties(node)


def importShibbolethPropertiesSettings(context):
    container = context.getSite()
    uf = getattr(aq_base(container), 'acl_users', None)

    if uf is not None:
        if 'shibproperties' not in uf.objectIds():
            manage_addShibUserProperties(uf)
        shibproperties = getattr(uf, 'shibproperties')
        importObjects(shibproperties, '', context)
