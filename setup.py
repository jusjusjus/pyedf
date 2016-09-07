
import os
import setuptools
from sys import platform
from textwrap import dedent



def ssl_available():
    """check if the C module can be build by trying to compile a small 
    program against the libssl development library"""

    import tempfile
    import shutil

    import distutils.sysconfig
    import distutils.ccompiler
    from distutils.errors import CompileError, LinkError

    libraries = ['ssl', 'crypto']

    # write a temporary .c file to compile
    c_code = dedent("""
    #include <openssl/md5.h>

    int main(int argc, char* argv[])
    {
    MD5_CTX mdContext;
        mdContext = mdContext;  /* prevent warning */
        return 0;
    }
    """)
    tmp_dir = tempfile.mkdtemp(prefix = 'tmp_pyedf_ssl_')
    bin_file_name = os.path.join(tmp_dir, 'test_ssl')
    file_name = bin_file_name + '.c'

    with open(file_name, 'w') as fp:
        fp.write(c_code)

    # and try to compile it
    compiler = distutils.ccompiler.new_compiler()
    assert isinstance(compiler, distutils.ccompiler.CCompiler)
    distutils.sysconfig.customize_compiler(compiler)

    try:
        compiler.link_executable(
            compiler.compile([file_name]),
            bin_file_name,
            libraries=libraries)

    except CompileError:
        print('libssl compile error.')
        ret_val = False

    except LinkError:
        print('libssl link error.')
        ret_val = False

    else:
        ret_val = True

    shutil.rmtree(tmp_dir)
    return ret_val



###



classifiers = [
"Development Status :: 4 - Beta",
"Intended Audience :: Science/Research",
"License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
"Programming Language :: C",
"Programming Language :: Python :: 2.7",
"Topic :: Scientific/Engineering :: Bio-Informatics"]


compile_args = ['-D_LARGEFILE64_SOURCE', '-D_LARGEFILE_SOURCE']
link_args = []


if ssl_available():
    compile_args.append('-DSSL')
    link_args.extend(['-lssl', '-lcrypto'])
    print("Compiling with SSL support.")



edf_module = setuptools.Extension('pyedf/recording/lib/_edf',
            sources            = ['src/edf.c', 'src/edflib.c'],
            extra_compile_args = compile_args,
            extra_link_args    = link_args)



setuptools.setup(
    name         = "pyedf",
    version      = "0.0.1",
    author       = "Justus Schwabedal",
    author_email = "JSchwabedal@gmail.com",
    description  = ("Python-bindings to the edf data format."),
    license      = "GPLv2",
    keywords     = "edf",
    url          = "https://github.com/jusjusjus/pyedf",
    packages     = ['pyedf', 'pyedf/recording', 'pyedf/derivation', 'pyedf/score'],
    ext_modules	 = [edf_module],
    classifiers	 = classifiers)
