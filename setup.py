from setuptools import setup, find_packages
import os

version = '0.8.6dev'

setup(name='pas.plugins.shibboleth',
      version=version,
      description="Shibboleth groups and properties handler for "
                  "Pluggable Authentication Service and PlonePAS",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='pas shibboleth plone',
      author='KULeuven ICTS',
      author_email='wms@icts.kuleuven.be',
      url=('https://github.com/KULeuven-WMS/pas.plugins.shibboleth.git'),
      license='GPL',
      package_dir={'': 'src'},
      packages=find_packages('src', exclude=['ez_setup']),
      namespace_packages=['pas', 'pas.plugins'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.PluggableAuthService',
          'Products.PlonePAS',
          'Products.GenericSetup',
      ],
      extras_require=dict(
         test=['plone.testing']))
