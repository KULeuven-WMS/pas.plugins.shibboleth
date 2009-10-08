# -*- coding: utf-8 -*-
"""
pas.plugins.shibboleth

Licensed under the GPL license, see LICENCE.txt for more details.

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
import unittest

from zope.testing import doctest
from zope.component import testing
from Products.PluggableAuthService.tests import pastc
from zope.configuration.xmlconfig import XMLConfig
from zope.app.testing import placelesssetup
from Testing.ZopeTestCase import FunctionalDocFileSuite
from pas.plugins.shibboleth import group
from pas.plugins.shibboleth.tests.base import ShibLayer

def test_suite():
    ftest = FunctionalDocFileSuite('README.txt',
                                   package="pas.plugins.shibboleth")
    ftest.layer = ShibLayer
    return unittest.TestSuite([ftest])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
