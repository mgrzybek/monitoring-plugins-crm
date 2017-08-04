import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name = "monitoring-plugins-crm",
	version = "1.0.1",
	author = "Mathieu Grzybek",
	author_email = "mathieu@grzybek.fr",
	description = "This script checks the state of resources and nodes.",
	license = "GPLv3",
	keywords = "monitoring check crm cluster",
	url = "https://github.com/mgrzybek/monitoring-plugins-crm",
	download_url = "https://github.com/mgrzybek/monitoring-plugins-crm/archive/1.0.1.tar.gz",
	packages = ['monitoring_plugins_crm'],
	data_files = [('/usr/lib/nagios/plugins',['bin/check_cluster'])],
	install_requires = ['pynagios'],
	long_description = read('README.rst'),
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Topic :: Utilities",
		"Environment :: Console",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
	]
)
