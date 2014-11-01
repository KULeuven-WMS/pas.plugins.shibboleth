# -*- coding: utf-8 -*-
"""
pas.plugins.shibboleth

Licensed under the GPL license, see LICENCE.txt for more details.
"""
import pas.plugins.shibboleth
from plone.testing import zca, z2, Layer


SHIB_WITH_ZCML = zca.ZCMLSandbox(name='SHIB_WITH_ZCML',
                                 package=pas.plugins.shibboleth,
                                 filename='testing.zcml')


class ShibbolethProduct(Layer):

    def setUp(self):
        with z2.zopeApp() as app:
            z2.installProduct(app, 'Products.PluggableAuthService')

SHIBBOLETH_PRODUCT = ShibbolethProduct(name='SHIBBOLETH_PRODUCT')
FUNCTIONAL_SHIB_WITH_ZCML = z2.FunctionalTesting(bases=(z2.STARTUP,
                                                        SHIB_WITH_ZCML,
                                                        SHIBBOLETH_PRODUCT),
                                                 name='FUNCTIONAL_SHIB_WITH_ZCML')  # NOQA
