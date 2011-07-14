# -*- coding: utf-8 -*-
"""
pas.plugins.shibboleth

Licensed under the GPL license, see LICENCE.txt for more details.

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
import unittest

from zope.testing import doctest
from pas.plugins.shibboleth.testing import FUNCTIONAL_SHIB_WITH_ZCML


OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    ftest = doctest.DocFileSuite('README.txt',
                                 package="pas.plugins.shibboleth",
                                 optionflags=OPTIONFLAGS)
    ftest.layer = FUNCTIONAL_SHIB_WITH_ZCML
    return unittest.TestSuite([ftest])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
