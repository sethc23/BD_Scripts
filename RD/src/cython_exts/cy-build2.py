
# run command: 'python cy-build.py build_ext -i'

from os import environ
environ["CC"] = "gcc" # may be specific to each computer
environ["CXX"] = "gcc"

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize


primarySource='getBestDG.pyx'
other_sources=['get_combo_start_info.pyx',
               'eval_single_order.pyx',
               'map_points_to_combos.pyx',
               'get_best_combo.pyx',
               'update_order_results.pyx']

if other_sources!=[]:
    a=[primarySource]
    a.extend(other_sources)
    ext_sources = a
else: ext_sources = [primarySource]

ext_modules=[
    Extension(name="getBestDG",
              sources=ext_sources)
]
setup( name='getBestDG',
       ext_modules = cythonize( ext_modules ))


from os import system
system('cython -a '+primarySource)