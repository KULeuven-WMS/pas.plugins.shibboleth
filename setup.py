from setuptools import setup, find_packages
import os

version = '0.6dev'

setup(name='pas.plugins.shibboleth',
      version=version,
      description="Shibboleth groups and properties handler for Pluggable Authentication Service and PlonePAS",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='pas shibboleth plone',
      author='KULeuven ICTS',
      author_email='wms@icts.kuleuven.be',
      url='https://wms.cc.kuleuven.be/repo2/wms/packages/pas.plugins.shibboleth',
      license='GPL',
      package_dir = {'': 'src'},
      packages=find_packages('src', exclude=['ez_setup']),
      namespace_packages=['pas', 'pas.plugins'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.PluggableAuthService',
          'Products.GenericSetup'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
