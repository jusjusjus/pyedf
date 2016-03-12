
import setuptools

edf_module = setuptools.Extension('recording/lib/_edf',
		sources=['recording/edf.c', 'recording/edflib.c'],
		extra_compile_args=['-D_LARGEFILE64_SOURCE', '-D_LARGEFILE_SOURCE'])

setuptools.setup(
	name = "pyedf",
	version = "0.0.2",
	author = "Justus Schwabedal",
	license = "GPL",
	packages = ['recording', 'derivation', 'score'],
	ext_modules = [edf_module])


