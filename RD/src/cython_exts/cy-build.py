
from os import environ
environ["CC"] = "gcc" # may be specific to each computer
environ["CXX"] = "gcc"

from distutils.core import setup
from distutils.extension import Extension
from Cython.Compiler.Main import default_options
default_options['emit_linenums'] = True
default_options['gdb_debug'] = False
default_options['working_path']='/Users/admin/SERVER2/BD_Scripts/RD/src/cython_exts/'
from Cython.Distutils import build_ext


extName='c_getBestDG'
extFile='getBestDG.pyx'
extSources = [extFile]


ext_modules = [Extension(name=extFile.rstrip('.py'),
                         sources=extSources,
                         #extra_compile_args=["-g"],
                         #extra_link_args=["-g"],
                         )]

setup(
  name =extName,
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules#,
  #gdb_debug=True
)



from os import system
system('cython -a '+extFile)

