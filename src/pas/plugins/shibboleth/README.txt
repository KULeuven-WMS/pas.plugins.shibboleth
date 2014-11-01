Set Up
------

Create a basic PAS folder in a new folder:

    >>> from pas.plugins.shibboleth.testing import FUNCTIONAL_SHIB_WITH_ZCML
    >>> app = FUNCTIONAL_SHIB_WITH_ZCML['app']
    >>> app.manage_addFolder('folder2')
    >>> folder = app.folder2
    >>> factory = folder.manage_addProduct['PluggableAuthService']
    >>> factory.addPluggableAuthService()
    >>> from Products.PluggableAuthService.interfaces.plugins import \
    ...   IAuthenticationPlugin, IUserEnumerationPlugin, IRolesPlugin, \
    ...   IRoleEnumerationPlugin, IRoleAssignerPlugin, \
    ...   IChallengePlugin, IExtractionPlugin, IUserAdderPlugin
    >>> pas = folder.acl_users
    >>> factory = pas.manage_addProduct['PluggableAuthService']
    >>> factory.addHTTPBasicAuthHelper('http_auth')
    >>> factory.addZODBUserManager('users')
    >>> factory.addZODBRoleManager('roles')
    >>> plugins = pas.plugins
    >>> plugins.activatePlugin(IChallengePlugin, 'http_auth')
    >>> plugins.activatePlugin(IExtractionPlugin, 'http_auth')
    >>> plugins.activatePlugin(IUserAdderPlugin, 'users')
    >>> plugins.activatePlugin(IAuthenticationPlugin, 'users')
    >>> plugins.activatePlugin(IUserEnumerationPlugin, 'users')
    >>> plugins.activatePlugin(IRolesPlugin, 'roles')
    >>> plugins.activatePlugin(IRoleAssignerPlugin, 'roles')
    >>> plugins.activatePlugin(IRoleEnumerationPlugin, 'roles')

Create our user:

    >>> from Testing.ZopeTestCase import user_name
    >>> from Testing.ZopeTestCase import user_password
    >>> from Testing.ZopeTestCase import user_role
    >>> uf = folder.acl_users
    >>> uf._doAddUser(user_name, user_password, [user_role], [])
    <PropertiedUser 'test_user_1_'>

Group Manager
-------------

Create the shib group manager:

    >>> from pas.plugins.shibboleth.group import manage_addShibGroupManager
    >>> manage_addShibGroupManager(uf, 'shibgroup')
    >>> shibGroupManager = uf.shibgroup


Activate our plugin:

    >>> from Products.PluggableAuthService.interfaces.plugins import IGroupsPlugin
    >>> plugins.activatePlugin(IGroupsPlugin, 'shibgroup')

Try to get the group from another user:

    >>> from Products.PluggableAuthService.plugins.tests.helpers import DummyUser
    >>> user = DummyUser('userid')
    >>> shibGroupManager.getGroupsForPrincipal(user)
    ()

Try to get the group from the current user *without* shibboleth headers:

    >>> user = uf.getUser(user_name)
    >>> shibGroupManager.getGroupsForPrincipal(user)
    ()

Now let's say that shibboleth has set the correct information in the REQUEST. We need to change the request:

    >>> app.REQUEST.environ['HTTP_KULOUNUMBER'] = '50649782'
    >>> user = uf.getUser(user_name)
    >>> shibGroupManager.getGroupsForPrincipal(user)
    ()

It still doesn't work because Shibboleth needs to provide the current logged in user information
inside the REQUEST:

    >>> app.REQUEST.environ['HTTP_EPPN'] = user_name
    >>> user = uf.getUser(user_name)
    >>> shibGroupManager.getGroupsForPrincipal(user)
    ('50649782',)

Same if we query all the plugins implementing IGroupsPlugin:

    >>> pas._getGroupsForPrincipal(user)
    ['50649782']

And with a user with more than 1 group:

    >>> app.REQUEST.environ['HTTP_KULOUNUMBER'] = '50649782;50649785'
    >>> shibGroupManager.getGroupsForPrincipal(user)
    ('50649782', '50649785')


User Properties
---------------

Create the shib user propeties manager:

    >>> from pas.plugins.shibboleth.property import manage_addShibUserProperties
    >>> manage_addShibUserProperties(uf, 'shib_user_props')
    >>> shibUserProps = uf.shib_user_props

Activate our plugin:

    >>> from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
    >>> plugins.activatePlugin(IPropertiesPlugin, 'shib_user_props')
    >>> plugins.listPlugins(IPropertiesPlugin)
    [('shib_user_props', <ShibUserPropertiesManager at /folder2/acl_users/shib_user_props>)]


By default the plugin will return an empty UserPropertySheet as Shibboleth didn't set anything in the
REQUEST headers

    >>> userPropertySheet = shibUserProps.getPropertiesForUser(user)
    >>> userPropertySheet
    <Products.PluggableAuthService.UserPropertySheet.UserPropertySheet instance ...>

    >>> userPropertySheet.propertyItems()
    []

Now let's say that shibboleth has set the correct information in the REQUEST. We need to change the request:

    >>> app.REQUEST.environ['HTTP_KULMAIL'] = 'info@kuleuven.be'
    >>> app.REQUEST.environ['HTTP_KULFULLNAME'] = 'John Foo'
    >>> userPropertySheet = shibUserProps.getPropertiesForUser(user)
    >>> userPropertySheet.propertyItems()
    []

Still nothing because we didn't set the properties on the object
    >>> shibUserProps.manage_addProperty('HTTP_KULMAIL', 'mail', 'string')
    >>> shibUserProps.manage_addProperty('HTTP_KULFULLNAME', 'fullname',
    ...                                  'string')
    >>> userPropertySheet = shibUserProps.getPropertiesForUser(user)
    >>> userPropertySheet.propertyItems()
    [('mail', 'info@kuleuven.be'), ('fullname', 'John Foo')]

Warning if one header is missing

    >>> from zope.testing.loggingsupport import InstalledHandler
    >>> handler = InstalledHandler('pas.plugins.shibboleth')
    >>> app.REQUEST.environ['HTTP_KULMAIL'] = 'info@kuleuven.be'
    >>> app.REQUEST.environ['HTTP_KULFULLNAME'] = ''
    >>> userPropertySheet = shibUserProps.getPropertiesForUser(user)
    >>> userPropertySheet.propertyItems()
    [('mail', 'info@kuleuven.be')]

We have something in the log:

    >>> len(handler.records)
    1
    >>> record = handler.records[0]
    >>> print record.name, record.levelname, record.getMessage()
    pas.plugins.shibboleth WARNING Property HTTP_KULFULLNAME has no value for user test_user_1_

Same if we query all the plugins implementing IPropertiesPlugin:

    >>> app.REQUEST.environ['HTTP_KULFULLNAME'] = 'John Foo'
    >>> propfinders = plugins.listPlugins( IPropertiesPlugin )
    >>> from Products.PluggableAuthService.interfaces.propertysheets import IPropertySheet
    >>> for propfinder_id, propfinder in propfinders:
    ...     data = propfinder.getPropertiesForUser(user)
    ...     if IPropertySheet.providedBy(data):
    ...         print data.propertyItems()
    ...     else:
    ...         print data
    [('mail', 'info@kuleuven.be'), ('fullname', 'John Foo')]


We can use the IUserPropertyFilter adapter to filter out values in the REQUEST
headers::

    >>> app.REQUEST.environ['HTTP_KULMAIL'] = ['foo@kuleuven.be', 'info@kuleuven.be']
    >>> def filterEmail(emails):
    ...     return emails[0]
    >>> from pas.plugins.shibboleth.interfaces import IUserPropertyFilter
    >>> from zope.component import provideAdapter
    >>> provideAdapter(filterEmail, adapts=(list, ), provides=IUserPropertyFilter,
    ...                name='HTTP_KULMAIL')

    >>> for propfinder_id, propfinder in propfinders:
    ...     data = propfinder.getPropertiesForUser(user)
    ...     if IPropertySheet.providedBy(data):
    ...         print data.propertyItems()
    ...     else:
    ...         print data
    [('mail', 'foo@kuleuven.be'), ('fullname', 'John Foo')]


User enumeration plugin
-----------------------

Once somebody login into Plone, CMF call getMemberById which calls PAS that
does a user enumeration. The shibboleth plugin is able to provide an
enumeration only for the logged in user and thus only replies if exact match is
True

Create the shib user propeties manager:

    >>> from pas.plugins.shibboleth.enumeration import manage_addShibUserEnumerationManager
    >>> manage_addShibUserEnumerationManager(uf, 'shib_user_enum')
    >>> shibUserEnumeration = uf.shib_user_enum

Activate our plugin:

    >>> from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
    >>> plugins.activatePlugin(IUserEnumerationPlugin, 'shib_user_enum')
    >>> plugins.listPlugins(IUserEnumerationPlugin)
    [('users', <ZODBUserManager at /folder2/acl_users/users>), ('shib_user_enum', <ShibUserEnumerationManager at /folder2/acl_users/shib_user_enum>)]

By default the plugin will return an empty tuple if the request don't have shib information:

    >>> shibUserEnumeration.enumerateUsers()
    ()

Even if was ask for the exact match:

    >>> shibUserEnumeration.enumerateUsers(login='foobar', exact_match=True)
    ()

Let's add some shibboleth informations inside the REQUEST:

    >>> app.REQUEST.environ['HTTP_EPPN'] = 'u007@kuleuven.be'

Non exact match doesnt return anything:

    >>> shibUserEnumeration.enumerateUsers()
    ()

Exact match for another user doesn't return anything:

    >>> shibUserEnumeration.enumerateUsers(login='u999999@kuleuven.be',
    ...                                    exact_match=True)
    ()

So it really returns info if we ask the enumerateUser for the logged in user:

    >>> shibUserEnumeration.enumerateUsers(login='u007@kuleuven.be',
    ...                                    exact_match=True)
    ({'login': 'u007@kuleuven.be', 'pluginid': 'shib_user_enum', 'id': 'u007@kuleuven.be'},)

And if we pass the id it should be the same:

    >>> shibUserEnumeration.enumerateUsers(id='u007@kuleuven.be',
    ...                                    exact_match=True)
    ({'login': 'u007@kuleuven.be', 'pluginid': 'shib_user_enum', 'id': 'u007@kuleuven.be'},)


Role Manager plugin
-------------------

Plone can also take into account that logged in user in Shibboleth should be considered as Member.
This is what the role manager plugin does.

Create the shib role manager:

    >>> from pas.plugins.shibboleth.role import manage_addShibRoleManager
    >>> manage_addShibRoleManager(uf, 'shib_role')
    >>> shibRole = uf.shib_role

Activate our plugin:

    >>> from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin
    >>> plugins.activatePlugin(IRolesPlugin, 'shib_role')
    >>> plugins.listPlugins(IRolesPlugin)
    [('roles', <ZODBRoleManager at /folder2/acl_users/roles>), ('shib_role', <ShibRoleManager at /folder2/acl_users/shib_role>)]

By default the plugin will return an empty tuple if the request don't have shib information:

Try to get the group from another user:

    >>> from Products.PluggableAuthService.plugins.tests.helpers import DummyUser
    >>> user = DummyUser('userid')
    >>> shibRole.getRolesForPrincipal(user)
    ()

Try to get the group from the current user *without* shibboleth headers:

    >>> from Testing.ZopeTestCase import user_name
    >>> user = uf.getUser(user_name)
    >>> shibRole.getRolesForPrincipal(user)
    ()

It still doesn't work because Shibboleth needs to provide the current logged in user information
inside the REQUEST:

    >>> app.REQUEST.environ['HTTP_EPPN'] = user_name
    >>> user = uf.getUser(user_name)
    >>> shibRole.getRolesForPrincipal(user)
    ('Member', 'Authenticated')
