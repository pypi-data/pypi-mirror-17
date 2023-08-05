#!/usr/bin/env python3
# pylint: disable=missing-docstring
import codecs
from setuptools import setup
try:
    codecs.lookup('mbcs')
except LookupError:
    def func(name, enc=codecs.lookup('ascii')):
        return {True: enc}.get(name == 'mbcs')
    codecs.register(func)


setup(name='gs_reply_bot',
      version='1.1.0',
      description='Automatic reply bot for GNU Social.',
      long_description=open('README.rst').read(),
      author='dtluna',
      author_email='dtluna@openmailbox.org',
      maintainer='dtluna',
      maintainer_email='dtluna@openmailbox.org',
      license='GPLv3',
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
      ],
      url='https://gitgud.io/dtluna/',
      platforms=['any'],
      install_requires=['gnusocial', 'pyxdg', 'py-config-parser'],
      scripts=['scripts/gs_reply_bot'])
