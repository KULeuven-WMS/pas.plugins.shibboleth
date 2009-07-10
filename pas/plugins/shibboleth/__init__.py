from Products.PluggableAuthService import registerMultiPlugin
from AccessControl.Permissions import add_user_folders
from pas.plugins.shibboleth import group
registerMultiPlugin(group.ShibGroupManager.meta_type)


def initialize(context):
    context.registerClass(group.ShibGroupManager,
                          permission = add_user_folders,
                          constructors = (
                              group.manage_addShibGroupManagerForm,
                              group.manage_addShibGroupManager),
                          visibility = None,
                          icon='')
