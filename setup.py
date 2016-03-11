
import setuptools

edf_module = setuptools.Extension('lib/_edf', sources=['src/edf.c', 'src/edflib.c'])

setuptools.setup(
	name = "pyedf",
	version = "0.0.2",
	author = "Justus Schwabedal",
	email = "jschwabedal@gmail.com",
	license = "GPL",
	packages = ['py'],
	ext_modules = [edf_module])


