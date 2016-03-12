
import setuptools



edf_module = setuptools.Extension('pyedf/recording/lib/_edf',
		sources=['pyedf/recording/edf.c', 'pyedf/recording/edflib.c'],
		extra_compile_args=['-D_LARGEFILE64_SOURCE', '-D_LARGEFILE_SOURCE'],
		extra_link_args=['-lssl', '-lcrypto'])



setuptools.setup(
	name = "pyedf",
	version = "0.0.2",
	author = "Justus Schwabedal",
	license = "GPL",
	packages = ['pyedf', 'pyedf/recording', 'pyedf/derivation', 'pyedf/score'],
	ext_modules = [edf_module])


