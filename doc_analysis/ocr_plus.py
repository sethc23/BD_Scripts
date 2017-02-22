#!env python
# coding: utf-8


'''
workon fileserver
cd ~/BD_Scripts/doc_analysis
ipython -i --pdb -c "$(
cat <<-'EOF'

from ocr_plus import *
df = pd.read_sql("""
        SELECT
            *
            ,_metadata->>'fpath' fpath
            ,_attr->>'word_info' word_info
        FROM file_idx
        WHERE (_metadata->>'fpath')::TEXT~*'DOC_IMAGES'::TEXT
        ORDER BY uid
    """,eng)
img_flist = df.fpath.astype(str).tolist()
ocr_content_confidences_images(img_flist)

EOF
)"

'''

import                                  pandas as pd
pd.set_option(                          'expand_frame_repr',False)
pd.set_option(                          'display.max_columns', None)
pd.set_option(                          'display.max_rows', 1000)
pd.set_option(                          'display.width',180)
np                              =       pd.np
np.set_printoptions(                    linewidth=200,threshold=np.nan)
from tesserocr                          import PyTessBaseAPI,PSM
from io                                 import BytesIO
from bs4                                import BeautifulSoup as BS
from IPython.display                    import HTML
html_template = """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
    <html>
    <head>
    <title>#TITLE#</title>
    <!--
    size: "3 px"; color: #0909CE; font : "20px arial,serif";
    colors:
        blue #0909CE
        green #368130
        black #000000
    -->


    <STYLE>
    .b { }
    .f_1 { size: "3 px"; color: #0909CE; font : "20px arial,serif"; font-style : "bold" }
    .f_2 { size: "2 px"; color: #000000 }
    .td_1 { width: 35px}
    .td_2 { }
    </STYLE>
    </head>
    <body>
    <!-- BODY CONTENT BELOW -->
    #BODY#
    <br>
    <!-- BODY CONTENT ABOVE -->
    </body>
    </html>
    """
import base64,json,os,sys,re
from subprocess                         import Popen as sub_popen
from subprocess                         import PIPE as sub_PIPE
import PIL

# sys.path.append('/home/ub2/BD_Scripts/doc_analysis/')

T = {'DB_NAME':'fileserver',
     'DB_HOST':'0.0.0.0',
     'DB_PORT':8800,
     'DB_USER':'postgres',
     'DB_PW':''}

def _load_connectors():
    eng                             =   create_engine(r'postgresql://%(DB_USER)s:%(DB_PW)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s'
                                                      % T,
                                                      encoding='utf-8',
                                                      echo=False)
    conn                            =   pg_connect("dbname='%(DB_NAME)s' host='%(DB_HOST)s' port=%(DB_PORT)s                                                    user='%(DB_USER)s' password='%(DB_PW)s' "
                                                   % T);
    cur                             =   conn.cursor()
    return eng,conn,cur


import logging
logger = logging.getLogger(             'sqlalchemy.dialects.postgresql')
logger.setLevel(logging.INFO)
from sqlalchemy                         import create_engine
from psycopg2                           import connect          as pg_connect
eng,conn,cur                    =   _load_connectors()

def to_sql(cmd):
    conn.set_isolation_level(    0)
    cur.execute(                 cmd)
def run_cmd(cmd):
    p = sub_popen(cmd,stdout=sub_PIPE,shell=True,executable='/bin/zsh')
    (_out,_err) = p.communicate()
    assert _err is None
    return _out.rstrip('\n')
def show_rotation_spacing(filename):
    """
    Automatically detect rotation and line spacing of an image of text using
    Radon transform
    If image is rotated by the inverse of the output, the lines will be
    horizontal (though they may be upside-down depending on the original image)
    It doesn't work with black borders
    """

    # from __future__ import division, print_function
    from skimage.transform import radon
    from PIL import Image
    from numpy import asarray, mean, array, blackman
    import numpy
    from numpy.fft import rfft
    import matplotlib.pyplot as plt
    from matplotlib.mlab import rms_flat
    try:
        # More accurate peak finding from
        # https://gist.github.com/endolith/255291#file-parabolic-py
        from parabolic import parabolic

        def argmax(x):
            return parabolic(x, numpy.argmax(x))[0]
    except ImportError:
        from numpy import argmax

    # Load file, converting to grayscale
    I = asarray(Image.open(filename).convert('L'))
    I = I - mean(I)  # Demean; make the brightness extend above and below zero
    plt.subplot(2, 2, 1)
    plt.imshow(I)

    # Do the radon transform and display the result
    sinogram = radon(I)

    plt.subplot(2, 2, 2)
    plt.imshow(sinogram.T, aspect='auto')
    plt.gray()

    # Find the RMS value of each row and find "busiest" rotation,
    # where the transform is lined up perfectly with the alternating dark
    # text and white lines
    r = array([rms_flat(line) for line in sinogram.transpose()])
    rotation = argmax(r)
    print('Rotation: {:.2f} degrees'.format(90 - rotation))
    plt.axhline(rotation, color='r')

    # Plot the busy row
    row = sinogram[:, rotation]
    N = len(row)
    plt.subplot(2, 2, 3)
    plt.plot(row)

    # Take spectrum of busy row and find line spacing
    window = blackman(N)
    spectrum = rfft(row * window)
    plt.plot(row * window)
    frequency = argmax(abs(spectrum))
    line_spacing = N / frequency  # pixels
    print('Line spacing: {:.2f} pixels'.format(line_spacing))

    plt.subplot(2, 2, 4)
    plt.plot(abs(spectrum))
    plt.axvline(frequency, color='r')
    plt.yscale('log')
    plt.show()
def crop_text_area(fpath,fpath_out):
    sys.path.append('/usr/local/lib/python2.7/dist-packages')
    import crop_morphology as CR_PG

    process_image(fpath, fpath_out)

    from IPython.display import Image
    Image(fpath)
    Image(fpath_out)
def ORIG_ocr_content_confidences_images():

    fpath='/home/ub2/ARCHIVE/DOC_IMAGES/038c69d2-0e3e-43e4-8ea9-274b93d2144b.jpg'
    fpath_out='/home/ub2/ARCHIVE/DOC_IMAGES/038c69d2-0e3e-43e4-8ea9-274b93d2144b_opencv.jpg'
    fpath='/home/ub2/ARCHIVE/MDSCAN/completed/__ppm__-31.ppm'
    fout='/home/ub2/ARCHIVE/MDSCAN/completed/__ppm__-31_opencv.pdf'

    fpath='/home/ub2/ARCHIVE/DOC_IMAGES/1482885785_8855e56.jpg'

    images = [fpath]
    r={}
    with PyTessBaseAPI() as api:
        for img in images:
            api.SetImageFile(img)
            r['lines']=api.GetTextlines()
            #r['images']=api.GetComponentImages()
            #r['thresh']=api.GetThresholdedImage()
            r['_words']=api.GetWords()
            r['strips']=api.GetStrips()
            r['text']=api.GetUTF8Text()
            r['words']=api.AllWords()
            r['word_conf']=api.AllWordConfidences()
            word_conf_map=api.MapWordConfidences()
            #r['word_conf_map']=api.MapWordConfidences()
            #print api.GetUTF8Text()
            #print api.AllWordConfidences()
    # api is automatically finalized when used in a with-statement (context manager).
    # otherwise api.End() should be explicitly called when it's no longer needed.

    def img_display(pil_image):
        b = BytesIO()
        pil_image.save(b, format='png')
        data = b.getvalue()
        r = '<img src="data:image/png;base64,' + base64.encodestring(data) + '"/>'
        return BS(r).renderContents().replace('&lt;','<').replace('&gt;','>').replace('\\n','\n')
        #return r
        #ip_img = display.Image(data=data, format='png', embed=True)
        #return ip_img._repr_png_()

    df=pd.DataFrame(map(lambda s: dict(zip(['word','conf'],s)),word_conf_map))
    df['images']=map(lambda i: r['_words'][i][0],range(len(r['_words'])))
    df['image2']=df.images.map(lambda img: img_display(img))
    h = df.sort_values(['conf','word'],ascending=[True,True]).head().ix[:,['conf','word','image2']].to_html(escape=True)
    HTML(BS(h).renderContents().replace('&lt;','<').replace('&gt;','>').replace('\\n','\n'))
def ocr_content_confidences_images(image_fpath_or_flist,conv_dict={},TO_SQL=True,RETURN_FIRST=False):
    def img_display(pil_image):
        b = BytesIO()
        pil_image.save(b, format='png')
        data = b.getvalue()
        r = '<img src="data:image/png;base64,' + base64.encodestring(data) + '"/>'
        # return BS(r).renderContents().replace('&lt;','<').replace('&gt;','>').replace('\\n','\n')
        return r

    if type(image_fpath_or_flist)==str:
        image_fpath_or_flist = [ image_fpath_or_flist ]

    with PyTessBaseAPI() as api:

        # MORE INFO:  https://tesseract.patagames.com/help/html/T_Patagames_Ocr_Enums_PageSegMode.htm
        # api.SetPageSegMode(PSM.SINGLE_COLUMN)
        # api.SetPageSegMode(PSM.SINGLE_BLOCK) # THIS SEEMS TO ENSURE len(GetWords)==len(MapWordConfidences)
        api.SetPageSegMode(PSM_AUTO)

        # api.SetVariable("tessedit_create_hocr", "1")
        api.SetVariable("tessedit_create_pdf", "1")
        # api.SetVariable("tessedit_write_unlv", "1")
        # api.SetVariable("tessedit_create_boxfile", "1")
        # api.SetVariable("tessedit_create_txt", "1")

        # api is automatically finalized when used in a with-statement (context manager).
        # otherwise api.End() should be explicitly called when it's no longer needed.
        for _fpath in image_fpath_or_flist:

            _fdir = os.path.dirname(_fpath)
            _fname = os.path.basename(_fpath)
            assert _fname.count('.')
            _fname_base = _fname[:_fname.rfind('.')]
            r = {}
            api.SetImageFile(_fpath)
            api.AnalyseLayout()
            api.Recognize()
            r['_words'] = api.GetWords()
            r['hocr'] = api.GetHOCRText(0)
            # r['text'] = api.GetUTF8Text()
            # r['btxt'] = api.GetBoxText(0)  # THIS IS THE BOX FILE DATA
            mean_conf = api.MeanTextConf()
            print(image_fpath_or_flist.index(_fpath),mean_conf,_fpath)
            word_conf_map = api.MapWordConfidences()
            df = pd.DataFrame(map(lambda s: dict(zip(['word_text','word_conf'],s)),word_conf_map))
            assert len(df)==len(r['_words'])
            df['word_image'] = map(lambda i: r['_words'][i][0],range(len(r['_words'])))
            df['word_image'] = df.word_image.map(lambda img: img_display(img))
            df['word_location'] = map(lambda i: r['_words'][i][1],range(len(r['_words'])))
            df['word_location'] = df['word_location'].map(lambda d: json.dumps(d))

            # h = df.sort_values(['conf','word'],ascending=[True,True]).head().ix[:,['conf','word','image2']].to_html(escape=True)
            # HTML(BS(h).renderContents().replace('&lt;','<').replace('&gt;','>').replace('\\n','\n'))

            _hocr_path = '/tmp/'+_fname_base + '.hocr'
            with open(_hocr_path, "wb") as f:  f.write(r['hocr'].encode("UTF-8"))
            _pdf_name = _fname_base + '.pdf'
            _pdf_save_path = '/'.join([ _fdir, _pdf_name ])


            #api.ProcessPage(_fdir,PIL.Image.open(_fpath),page_index=1,filename=_pdf_name)

            """
            convert -deskew 40% test_pnm_conv_morphed.jpg \
                jpegtopnm - | pnmtotiff - | \
                tesseract - - pdf|pdftotext -layout - -
            """

            c = """
                ENV="/home/ub2/SERVER2/ipy_jupyter/ENV"
                source $ENV/bin/activate
                # UUID="${$(uuidgen -r):1:7}"
                # TMP="/tmp/$UUID"
                # mkdir $TMP
                # cd $TMP
                # mv %(_hocr_path)s ./
                # cp %(_fpath)s ./
                # hocr-pdf ./ > %(_pdf_save_path)s
                # cd ..
                # rm -fr $TMP
                pdftotext -layout %(_pdf_save_path)s - | base64
                """ % locals()
            cmd = '\n'.join( [ re.sub(r'^([\s\t\n]+)(.*)$',r'\2',it) for it in c.split('\n')[1:-1] ] ) + '\n'
            ocr_text_x64 = run_cmd( cmd )

            if TO_SQL:
                c = ''.join([
                        "UPDATE file_idx SET "
                        ,"_attr='"
                        ,json.dumps({
                            'word_info' : json.dumps(df.to_dict('index')).replace("'","''")
                            })
                        ,"'::JSON "
                        ,",_content='"
                        ,ocr_text_x64
                        ,"'::TEXT "
                        ,"WHERE uid=" + conv_dict[_fpath]
                    ])
                to_sql(c)

            if RETURN_FIRST:
                return df,mean_conf,ocr_text_x64


        return

def ipy_test():
    image_fpath_or_flist = '/home/ub2/ARCHIVE/DOC_IMAGES/1482885785_8855e56.jpg'
    ocr_content_confidences_images(image_fpath_or_flist)


    # get_ipython().magic(u'sql SELECT * FROM file_idx ORDER BY last_updated DESC LIMIT 1')
    # print pd.read_sql("SELECT _content r FROM file_idx ORDER BY last_updated DESC LIMIT 1",eng).r.tolist()[0]

    df = pd.read_sql("select *,_attr->>'word_info' word_info,((_attr->>'word_info')::jsonb)->>'word_image' word_image from file_idx order by last_updated desc limit 1",eng)
    # h = df.sort_values(['conf','word'],ascending=[True,True]).head().ix[:,['conf','word','image2']].to_html(escape=True)
    # h = df.to_html(escape=True)
    # HTML(BS(h).renderContents().replace('&lt;','<').replace('&gt;','>').replace('\\n','\n'))

    # SHOW IMAGES (using results from query)
    D = json.loads(df.word_info.tolist()[0])
    cols = D['0'].keys()
    nf = pd.DataFrame(columns=cols)
    for k in sorted([int(_k) for _k in D.keys()]):
        nf = nf.append(D[str(k)],ignore_index=True)

    HTML(BS(nf.style.render()).renderContents().replace('&lt;','<').replace('&gt;','>').replace('\\n','\n'))

    # # SHOW IMAGES (when initially creating dataframe)
    # h = pd.DataFrame(data=dict(zip(D.keys(),D.values()))).to_html(escape=True)
    # HTML(BS(h).renderContents().replace('&lt;','<').replace('&gt;','>').replace('\\n','\n'))

def main():
    DIR=os.environ['HOME'] + '/ARCHIVE/DOC_IMAGES'
    fpaths = [DIR+'/'+it for it in os.listdir(DIR)]
    pdfs_as_jpgs = [ re.sub(r'(.*)/(.*)[.]([^\.]{,4})$',r'\1/\2',it)+'.jpg' for it in fpaths if it.count('.pdf')]
    df = pd.read_sql("""
            SELECT
                uid
                ,_metadata->>'fpath' fpath
            FROM file_idx
            WHERE (_metadata->>'fpath')::TEXT ~* 'DOC_IMAGES'::TEXT
            ORDER BY uid
        """,eng)
    idx = df[df.fpath.isin(pdfs_as_jpgs)==False].index.tolist()
    img_fpaths = df.ix[idx,'fpath'].astype(str).tolist()
    img_uids = df.ix[idx,'uid'].astype(str).tolist()
    fpath_uid_dict = dict(zip(img_fpaths,img_uids))
    print(len(img_fpaths))
    ocr_content_confidences_images(img_fpaths,fpath_uid_dict)

# Dynamically call functions
if __name__ == '__main__':
    from sys import argv
    args = argv[1:]

    if not args:
        raise SystemExit
    else:
        import sys
        if len(args)>1:
            if type(args[-1])==dict:
                getattr(sys.modules[__name__],args[0])(args[1:-1],args[-1])
            else:
                getattr(sys.modules[__name__],args[0])(args[1:])
        else:
            getattr(sys.modules[__name__],args[0])()