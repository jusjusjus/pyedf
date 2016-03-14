
import setuptools
from sys import platform

if platform == "linux" or platform == "linux2" or platform == "darwin":
	link_args = ['-lssl', '-lcrypto']

else:
	link_args = []

edf_module = setuptools.Extension('pyedf/recording/lib/_edf',
		sources=['pyedf/recording/edf.c', 'pyedf/recording/edflib.c'],
		extra_compile_args=['-D_LARGEFILE64_SOURCE', '-D_LARGEFILE_SOURCE'],
		extra_link_args=link_args)



setuptools.setup(
	name = "pyedf",
	version = "0.0.1",
	author = "Justus Schwabedal",
	author_email = "JSchwabedal@gmail.com",
	description = ("Python-bindings to the edf data format."),
	license = "GPLv2",
	keywords = "edf",
	url = "https://github.com/jusjusjus/pyedf",
	packages = ['pyedf', 'pyedf/recording', 'pyedf/derivation', 'pyedf/score'],
	ext_modules = [edf_module],
	classifiers = ["Development Status :: 4 - Beta",
			"Intended Audience :: Science/Research",
			"License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
			"Programming Language :: C",
			"Programming Language :: Python :: 2.7",
			"Topic :: Scientific/Engineering :: Bio-Informatics"])


