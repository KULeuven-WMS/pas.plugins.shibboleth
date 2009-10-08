# -*- coding: utf-8 -*-
"""
pas.plugins.shibboleth

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
from Products.GenericSetup.testing import BodyAdapterTestCase
from pas.plugins.shibboleth.tests.base import ShibLayer

_PROPERTIES_BODY = u"""<?xml version="1.0"?>
<shibproperties>
 <property name="HTTP_FOO" type="string">bar</property>
 <property name="HTTP_FULLNAME" type="string">fullname</property>
</shibproperties>
""".encode('utf-8')


class PropertiesXMLAdapterTests(BodyAdapterTestCase):
    layer = ShibLayer

    def _getTargetClass(self):
        from pas.plugins.shibboleth.exportimport import ShibPropertiesXMLAdapter
        return ShibPropertiesXMLAdapter

    def _populate(self, obj):
        obj._setProperty('HTTP_FOO', 'bar', 'string')
        obj._setProperty('HTTP_FULLNAME', 'fullname', 'string')

    def _verifyImport(self, obj):
        self.assertEqual(type(obj.HTTP_FOO), str)
        self.assertEqual(obj.HTTP_FOO, 'bar')
        self.assertEqual(type(obj.HTTP_FULLNAME), str)
        self.assertEqual(obj.HTTP_FULLNAME, 'fullname')

    def setUp(self):
        from pas.plugins.shibboleth.property import ShibUserPropertiesManager
        BodyAdapterTestCase.setUp(self)
        self._obj = ShibUserPropertiesManager('foo')
        self._BODY = _PROPERTIES_BODY


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(PropertiesXMLAdapterTests))
    return suite
