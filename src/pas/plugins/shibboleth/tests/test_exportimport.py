# -*- coding: utf-8 -*-
"""
pas.plugins.shibboleth

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
from unittest import TestCase
from zope.component import getMultiAdapter
from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.testing import DummySetupEnviron
from pas.plugins.shibboleth.testing import SHIB_WITH_ZCML

_PROPERTIES_BODY = u"""<?xml version="1.0"?>
<shibproperties>
 <property name="HTTP_FOO" type="string">bar</property>
 <property name="HTTP_FULLNAME" type="string">fullname</property>
</shibproperties>
""".encode('utf-8')


class BodyAdapterTestCase(TestCase):

    def test_body_get(self):
        self._populate(self._obj)
        context = DummySetupEnviron()
        adapted = getMultiAdapter((self._obj, context), IBody)
        self.assertEqual(adapted.body, self._BODY)

    def test_body_set(self):
        context = DummySetupEnviron()
        adapted = getMultiAdapter((self._obj, context), IBody)
        adapted.body = self._BODY
        self._verifyImport(self._obj)
        self.assertEqual(adapted.body, self._BODY)

        # now in update mode
        context._should_purge = False
        adapted = getMultiAdapter((self._obj, context), IBody)
        adapted.body = self._BODY
        self._verifyImport(self._obj)
        self.assertEqual(adapted.body, self._BODY)

        # and again in update mode
        adapted = getMultiAdapter((self._obj, context), IBody)
        adapted.body = self._BODY
        self._verifyImport(self._obj)
        self.assertEqual(adapted.body, self._BODY)


class PropertiesXMLAdapterTests(BodyAdapterTestCase):
    layer = SHIB_WITH_ZCML

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
