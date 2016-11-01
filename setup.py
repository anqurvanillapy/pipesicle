# -*- coding: utf-8 -*-

from postocol import __version__
from setuptools import setup


setup(
    name='postocol',
    version=__version__,
    description='Abstract class for creating homemade static site generator',
    license='MIT',
    url='http://github.com/anqurvanillapy/postocol/',
    author='AnqurVanillapy',
    author_email='anqurvanillapy@gmail.com',
    packages=['postocol'],
    install_requires=['Jinja2>=2.8'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
