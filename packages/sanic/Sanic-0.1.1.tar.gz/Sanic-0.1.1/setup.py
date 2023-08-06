"""
Sanic
"""
from setuptools import setup

setup(
    name='Sanic',
    version="0.1.1",
    url='http://github.com/channelcat/sanic/',
    license='BSD',
    author='Channel Cat',
    author_email='channelcat@gmail.com',
    description='A microframework based on uvloop, httptools, and learnings of flask',
    packages=['sanic'],
    platforms='any',
    install_requires=[
        'uvloop>=0.5.3',
        'httptools>=0.0.9',
        'ujson>=1.35',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
    ],
)
