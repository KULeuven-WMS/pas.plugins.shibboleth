Set Up
------

Load all of Five's configuration (this is a functional test):

    >>> import Products.Five
    >>> from Products.Five.zcml import load_config
    >>> load_config('configure.zcml', package=Products.Five)

Initialize our package for zope:

    >>> import pas.plugins.shibboleth
    >>> load_config('configure.zcml', package=pas.plugins.shibboleth)

Create a basic PAS folder in a new folder:

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

And with a user with more than 1 group:

    >>> app.REQUEST.environ['HTTP_KULOUNUMBER'] = '50649782;50649785'
    >>> shibGroupManager.getGroupsForPrincipal(user)
    ('50649782', '50649785')

