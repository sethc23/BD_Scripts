"""
    Page segmentation modes:
      0    Orientation and script detection (OSD) only.
      1    Automatic page segmentation with OSD.
      2    Automatic page segmentation, but no OSD, or OCR.
      3    Fully automatic page segmentation, but no OSD. (Default)
      4    Assume a single column of text of variable sizes.
      5    Assume a single uniform block of vertically aligned text.
      6    Assume a single uniform block of text.
      7    Treat the image as a single text line.
      8    Treat the image as a single word.
      9    Treat the image as a single word in a circle.
     10    Treat the image as a single character.
"""

import os
from ctypes import *

lang = "eng"

fpath = "/home/ub2/ARCHIVE/DOC_IMAGES/test_pnm_conv_morphed_deskewed.tiff"

fdir = os.path.dirname(fpath)
fname = os.path.basename(fpath)
assert fname.count('.'),'ERROR:  missing extension separator "." from file: ' + fname
fbase = fname[:fname.rfind('.')]
f_out_base = fdir + '/' + fbase

TESSDATA_PREFIX = os.environ.get('TESSDATA_PREFIX')
if not TESSDATA_PREFIX:
    TESSDATA_PREFIX = "/usr/local/share/tessdata"

tess_libpath = "/usr/local/lib/libtesseract.so.4.0.0"
TESS = cdll.LoadLibrary(tess_libpath)
TESS.TessVersion.restype = c_char_p
tesseract_version = TESS.TessVersion()
print('Tesseract-ocr version:', tesseract_version)

lept_libpath = "/usr/local/lib/liblept.so.5.0.1"
LEPT = cdll.LoadLibrary(lept_libpath)
LEPT.getLeptonicaVersion.restype = c_char_p
leptonica_version = LEPT.getLeptonicaVersion()
print('Leptonica version:', leptonica_version)

# getImagelibVersions()
# print('Leptonica Version: %s.%s.%s' % (L.LIBLEPT_MAJOR_VERSION,L.LIBLEPT_MINOR_VERSION,L.LIBLEPT_PATCH_VERSION))


class TessBaseAPI(Structure):
    pass
class TessResultRenderer(Structure):
    pass
class Pix(Structure):
    pass

TESS.TessBaseAPICreate.restype = POINTER(TessBaseAPI)
TESS.TessBaseAPIInit3.argtypes = [POINTER(TessBaseAPI), c_char_p, c_char_p]
TESS.TessBaseAPIInit3.restype = c_bool
TESS.TessBaseAPIProcessPage.argtypes = [POINTER(TessBaseAPI), POINTER(Pix), c_int, c_char_p, c_char_p, c_int, POINTER(TessResultRenderer)]
TESS.TessBaseAPIProcessPage.restype = c_bool
TESS.TessBaseAPIProcessPages.argtypes = [POINTER(TessBaseAPI), c_char_p, c_char_p, c_int, POINTER(TessResultRenderer)]
TESS.TessBaseAPIProcessPages.restype = c_bool
TESS.TessBaseAPIGetUTF8Text.argtypes = [POINTER(TessBaseAPI)]
TESS.TessBaseAPIGetUTF8Text.restype = c_char_p

# TESS.TessResultRenderer.argtypes = [POINTER(TessResultRenderer),c_char_p, c_char_p]
# TESS.TessResultRenderer.restype = c_void

TESS.TessPDFRendererCreate.argtypes = [c_char_p, c_char_p]
TESS.TessPDFRendererCreate.restype = POINTER(TessResultRenderer)
TESS.TessResultRendererBeginDocument.argtypes = [POINTER(TessResultRenderer),c_char_p ]
TESS.TessResultRendererBeginDocument.restype = c_bool
TESS.TessResultRendererAddImage.argtypes = [POINTER(TessResultRenderer), POINTER(TessBaseAPI)]
TESS.TessResultRendererAddImage.restype = c_bool
TESS.TessResultRendererEndDocument.argtypes = [POINTER(TessResultRenderer)]
TESS.TessResultRendererEndDocument.restype = c_bool
TESS.TessDeleteResultRenderer.argtypes = [POINTER(TessResultRenderer)]
TESS.TessDeleteResultRenderer.restype = c_void_p

LEPT.pixRead.argtypes = [c_char_p]
LEPT.pixRead.restype = POINTER(Pix)

API = TESS.TessBaseAPICreate()
RES = TESS.TessPDFRendererCreate(f_out_base, TESSDATA_PREFIX)

rc = TESS.TessBaseAPIInit3(API, TESSDATA_PREFIX, lang)
if (rc):
    TESS.TessBaseAPIDelete(API)
    print("Could not initialize tesseract.\n")
    exit(3)

TESS.TessBaseAPISetPageSegMode(API,3)
IMAGE = LEPT.pixRead(fpath)
# TESS.TessBaseAPISetImage2(API,IMAGE)
# TESS.TessBaseAPISetSourceResolution(API,150)
# TESS.TessBaseAPIAnalyseLayout(API)

# status = TESS.TessResultRendererBeginDocument(RES,fname)
# status = TESS.TessResultRendererAddImage(RES,API)
# status = TESS.TessResultRendererEndDocument(RES)

# success = TESS.TessBaseAPIProcessPage(API, IMAGE, 1, fpath, None , 0, RES)
success = TESS.TessBaseAPIProcessPages(API, fpath, None , 0, RES)
print('success:',success)
# if success:

    # status = TESS.TessResultRendererBeginDocument(RES,fname)
    # print('1status:',status)
    # # status = TESS.TessResultRendererAddImage(RES,API)
    # # print('2status:',status)
    # status = TESS.TessResultRendererEndDocument(RES)
    # print('3status:',status)
    # status = TESS.TessDeleteResultRenderer(RES)
    # print('4status:',status)
    # text = TESS.TessBaseAPIGetUTF8Text(api)
    # print("="*78)
    # print(text.decode("utf-8").strip())
    # print("="*78)


# IMAGE = LEPT.pixRead(fpath)

# TESS.TessBaseAPISetPageSegMode(api,3)
# # TESS.TessBaseAPISetVariable("tessedit_create_pdf", 1)
# # TESS.TessBaseAPISetVariable("tessedit_create_hocr", "1")
# # TESS.TessBaseAPISetVariable("tessedit_create_boxfile", "1")
# # TESS.TessBaseAPISetVariable("tessedit_create_txt", "1")

# TESS.TessBaseAPISetImage2(api,IMAGE)
# TESS.TessBaseAPISetSourceResolution(api,150)

# TESS.TessBaseAPIAnalyseLayout(api)

# # res = ITessAPI.TessResultRenderer()
# # res.TessBoxTextRendererCreate(f_out_base)
# # res.TessHOcrRendererCreate(fdir)

# res = TESS.TessPDFRendererCreate(fdir, TESSDATA_PREFIX)
# status = TESS.TessBaseAPIProcessPage(api, IMAGE, 1, fpath, None, 0,res)
# print('status:',status)

# words = TESS.TessBaseAPIGetUTF8Text(api)
# print('WORDS:',string_at(words))

# hocr = TESS.TessBaseAPIGetHOCRText(api, 1)
# print('HOCR:',string_at(hocr))

# mean_conf = TESS.TessBaseAPIMeanTextConf(api)
# print('MEAN_CONF:',mean_conf)

# word_conf = TESS.TessBaseAPIAllWordConfidences(api)
# print('WORD_CONF:',string_at(word_conf))

# text_out = TESS.TessBaseAPIProcessPages(api, fpath, None, 0)
# print('TEXT_OUT:',string_at(mean_conf))





# TESS.TessDeleteResultRenderer(RES)

TESS.TessBaseAPIEnd(API)
# LEPT.lept_fclose(fpath)
