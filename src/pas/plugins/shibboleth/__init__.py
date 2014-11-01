# -*- coding: utf-8 -*-
from Products.PluggableAuthService import registerMultiPlugin
from AccessControl.Permissions import add_user_folders
from pas.plugins.shibboleth import group, property, enumeration, role


registerMultiPlugin(group.ShibGroupManager.meta_type)
registerMultiPlugin(property.ShibUserPropertiesManager.meta_type)
registerMultiPlugin(enumeration.ShibUserEnumerationManager.meta_type)
registerMultiPlugin(role.ShibRoleManager.meta_type)


def initialize(context):
    context.registerClass(group.ShibGroupManager,
                          permission=add_user_folders,
                          constructors=(
                              group.manage_addShibGroupManagerForm,
                              group.manage_addShibGroupManager),
                          visibility=None,
                          icon='')
    context.registerClass(property.ShibUserPropertiesManager,
                          permission=add_user_folders,
                          constructors=(
                              property.manage_addShibUserPropertiesManagerForm,
                              property.manage_addShibUserProperties),
                          visibility=None,
                          icon='')
    context.registerClass(enumeration.ShibUserEnumerationManager,
                          permission=add_user_folders,
                          constructors=(
                              enumeration.manage_addShibUserEnumerationManagerForm,
                              enumeration.manage_addShibUserEnumerationManager),
                          visibility=None,
                          icon='')
    context.registerClass(role.ShibRoleManager,
                          permission=add_user_folders,
                          constructors=(
                              role.manage_addShibRoleManagerForm,
                              role.manage_addShibRoleManager),
                          visibility=None,
                          icon='')
