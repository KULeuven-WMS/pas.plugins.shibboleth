# -*- coding: utf-8 -*-
"""
pas.plugins.shibboleth

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
import os
from zope.app.testing.functional import ZCMLLayer
import pas.plugins.shibboleth

testingZCMLPath = os.path.join(os.path.dirname(__file__), 'testing.zcml')
ShibLayer = ZCMLLayer(testingZCMLPath,
                      'arsia.cerise.compta.impressions',
                      'CeriseComptaImpressions')


