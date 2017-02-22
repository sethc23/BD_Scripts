#!python
#cython: c_string_type=unicode, c_string_encoding=utf-8


"""

    python cy_build.py build_ext --force --debug --verbose -i; cython -a c_tesseract.pyx

"""

# print('ok')


# import pyximport#,pp
# pyximport.install(build_in_temp=False,inplace=True)
# import Cython.Compiler.Options
# Cython.Compiler.Options.annotate = True

# print(dir())

from tesseract cimport *
from libc.stdlib cimport malloc, free
from cpython.version cimport PY_MAJOR_VERSION
# cimport tesseract

cdef bytes _b(s):
    if PY_MAJOR_VERSION > 3:
        if isinstance(s, str):
            return s.encode('UTF-8')
    elif isinstance(s, unicode):
        return s.encode('UTF-8')
    return s



# default parameters
# setMsgSeverity(L_SEVERITY_NONE)  # suppress leptonica error messages
cdef TessBaseAPI _api = TessBaseAPI()
# _api.SetVariable('debug_file', '/dev/null')  # suppress tesseract debug messages
# _api.Init(NULL, NULL)
# cdef _DEFAULT_PATH = abspath(join(_api.GetDatapath(), os.pardir)) + os.sep
# cdef _DEFAULT_LANG = _api.GetInitLanguagesAsString()
# _api.End()
# TessBaseAPI.ClearPersistentCache()

# def tesseract_version():
#     """Return tesseract-ocr and leptonica version info"""
#     version_str = u"tesseract {}\n {}\n  {}"
#     tess_v = TessBaseAPI.Version()
#     lept_v = _free_str(getLeptonicaVersion())
#     libs_v = _free_str(getImagelibVersions())
#     return version_str.format(tess_v, lept_v, libs_v)



# cdef cchar_t *text = TessVersion()
# cdef void printf(TessVersion())

cdef unicode _free_str(char *text):
    """Return unicode string and free the c pointer"""
    try:
        return text
    finally:
        free(text)

# from libc.stdio cimport printf
# _version = TessVersion()

# cdef:
#     TessBaseAPI baseapi
#     char *version_str

# printf(TessBaseAPI.Version())
# printf(leptonica.getLeptonicaVersion())
# printf(leptonica.getImagelibVersions())

# def tesseract_version():
#     """Return tesseract-ocr and leptonica version info"""

#     version_str = u"tesseract {}\n {}\n  {}"
#     tess_v = TessBaseAPI.Version()
#     lept_v = _free_str(getLeptonicaVersion())
#     libs_v = _free_str(getImagelibVersions())
#     # printf(version_str.format(tess_v, lept_v, libs_v))
#     return version_str.format(tess_v, lept_v, libs_v)

# _version=tesseract_version()
# printf(_version)

# print(tesseract_version())

# from libcpp.string cimport string
# from libcpp.vector cimport vector

# cdef string s = tesseract_version()
# print(s)
# cpp_string = <string> tesseract_version().encode('utf-8')

# cdef vector[int] vect = xrange(1, 10, 2)
# print(vect)              # [1, 3, 5, 7, 9]

# cdef vector[string] cpp_strings = b'ab cd ef gh'.split()
# print(cpp_strings[1])   # b'cd'



# cdef class PyTessBaseAPI:
#     """Cython wrapper class around the C++ TessBaseAPI class.

#     Usage as a context manager:

#     >>> with PyTessBaseAPI(path='./', lang='eng') as tesseract:
#     ...     tesseract.SetImage(image)
#     ...     text = tesseract.GetUTF8Text()

#     Example with manual handling:

#     >>> tesseract = PyTessBaseAPI(path='./', lang='eng')
#     >>> try:
#     ...     tesseract.SetImage(image)
#     ...     text = tesseract.GetUTF8Text()
#     ... finally:
#     ...     tesseract.End()

#     Args:
#         path (str): The name of the parent directory of tessdata.
#             Must end in /.
#         lang (str): An ISO 639-3 language string. Defaults to 'eng'.
#             The language may be a string of the form [~]<lang>[+[~]<lang>]* indicating
#             that multiple languages are to be loaded. Eg hin+eng will load Hindi and
#             English. Languages may specify internally that they want to be loaded
#             with one or more other languages, so the ~ sign is available to override
#             that. Eg if hin were set to load eng by default, then hin+~eng would force
#             loading only hin. The number of loaded languages is limited only by
#             memory, with the caveat that loading additional languages will impact
#             both speed and accuracy, as there is more work to do to decide on the
#             applicable language, and there is more chance of hallucinating incorrect
#             words.
#         psm (int): Page segmentation mode. Defaults to :attr:`PSM.AUTO`.
#             See :class:`PSM` for avaialble psm values.
#         init (bool): If ``False``, :meth:`Init` will not be called and has to be called
#             after initialization.

#     Raises:
#         :exc:`RuntimeError`: If `init` is ``True`` and API initialization fails.
#     """

#     cdef:
#         TessBaseAPI _baseapi
#         Pix *_pix

#     @staticmethod
#     def Version():
#         return TessBaseAPI.Version()

