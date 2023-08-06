import sys
#from distutils.core import setup, Extension
from setuptools import setup,Extension,find_packages
version = sys.version_info

with open("README.md", "r") as fh:
	long_description = fh.read()

setup (name = 'kvrocks_scan',
	version = '1.0',
	description = 'kvrocks_scan',
	long_description=long_description,
	long_description_content_type="text/markdown",
	author = "lyramilk",
	packages=[''],
	install_requires = ['redis>=0.3'],
	author_email='lyramilk@qq.com',
	license='Apache License 2.0',
	url='https://github.com/lyramilk/kvrocks_scan', 
	classifiers=[
		"Intended Audience :: Developers",
		"Operating System :: OS Independent",
		"Natural Language :: Chinese (Simplified)",
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.5',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Topic :: Utilities'
	],
	keywords = 'kvrocks,redis',
)