#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
    packages = find_packages()

except ImportError:
    from distutils import setup
    packages = ['reports', 'reports.config']

from reports import __version__ as version

setup(name='reports',
      version=version,
      description='Assists in querying github repos',
      license='LICENSE',
      author_email='lcampbell@asascience.com',
      package_data = {
          '': ['*.yml']
      },
      packages=packages,
      setup_requires=[
          'requests',
          'python-dateutil',
          'PyYAML'
      ])



