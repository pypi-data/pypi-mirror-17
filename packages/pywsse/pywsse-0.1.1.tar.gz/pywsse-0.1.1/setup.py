# setup.py
# coding=utf-8
# py-wsse
# Authors: Rushy Panchal, Naphat Sanguansin, Adam Libresco, Jérémie Lumbroso
# Date: August 31st, 2016
# Description: Setuptools configuration.

from setuptools import setup

setup(
	name = 'pywsse',
	packages = [
		'wsse',
		'wsse.server',
		'wsse.server.django',
		'wsse.server.drf',
		'wsse.server.default',
		'wsse.client',
		'wsse.client.requests',
		],
	version = '0.1.1',
	description = 'WSSE Authentication for various server and client backends.',
	author = 'Rushy Panchal',
	author_email = 'rushy.panchal@princeton.edu',
	url = 'https://github.com/PrincetonUniversity/py-wsse',
	keywords = ['rest', 'authentication', 'wsse'],
	license = 'LGPLv3',
	classifiers = [
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.1',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Intended Audience :: Developers',
		'Operating System :: OS Independent',
		'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
		],
	tests_require = [
		'nose',
		'mock>=2.0.0',
		'django>=1.9',
		'djangorestframework>=3.4.6',
		'requests>=2.11.1',
		],
	test_suite = 'nose.collector',
)
