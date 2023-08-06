#!/usr/bin/env python
"""
Erply-API
---------

Python wrapper for Erply API
"""
from distutils.core import setup

setup(
    name='ErplyAPI',
    version='0.2016.09.12',
    description='Python wrapper for Erply API',
    license='BSD',
    author='Priit Laes',
    author_email='plaes@plaes.org',
    long_description=__doc__,
    install_requires=['requests'],
    py_modules=['erply_api'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Office/Business :: Financial :: Point-Of-Sale',
        'Topic :: Software Development :: Libraries',
    ]
)
