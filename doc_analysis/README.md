# Doc Analysis
---

### [Tesseract](https://github.com/tesseract-ocr/tesseract/wiki/Compiling)
- [API Examples](https://github.com/tesseract-ocr/tesseract/wiki/APIExample)
- [C-API Reference (v. 4.0)](https://tesseract-ocr.github.io/a00638.html#af05c5f7be48946d521660f05323417e7)
- [C-API Reference (v. 3.0)](http://tess4j.sourceforge.net/docs/docs-3.0/net/sourceforge/tess4j/TessAPI1.html)
- [User Notes for C-API](http://stackoverflow.com/questions/30688840/access-confidence-in-python-tesseract)
- ##### Training:
  - [Terese: A Tesseract Correction Tool](http://terese.sourceforge.net/)
  - [HTML editor](https://github.com/tmbdev/ocropy/wiki/Working-with-Ground-Truth)
  - Tesseract's [ScrollView.jar](https://github.com/tesseract-ocr/tesseract/wiki/ViewerDebugging)

- ##### Install:
  ```bash
  export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig/:/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/lib/pkgconfig/
  export LD_LIBRARY_PATH=/usr/local/lib/ 
  export LD_RUN_PATH=/usr/local/lib
  sudo ldconfig -v
  export LEPTONICA_LIBS="-L/usr/local/lib -llept"
  export LEPTONICA_CFLAGS="-I/usr/local/include/leptonica"
  git clone https://github.com/tesseract-ocr/tesseract.git
  cd tesseract && ./autogen.sh
  ./configure --enable-debug --enable-opencl
  LDFLAGS="-L/usr/local/lib" CFLAGS="-I/usr/local/include" make
  make install
  unset LEPTONICA_LIBS && unset LEPTONICA_CFLAGS
  
  sudo ldconfig
  
  make training
  sudo make training-install
  
  cd java
  wget -L -o piccolo2d-core-3.0.jar http://search.maven.org/remotecontent?filepath=org/piccolo2d/piccolo2d-core/3.0/piccolo2d-core-3.0.jar
  wget -L -o piccolo2d-extras-3.0.jar http://search.maven.org/remotecontent\?filepath\=org/piccolo2d/piccolo2d-extras/3.0/piccolo2d-extras-3.0.jar
  make ScrollView.jar
  
  export SCROLLVIEW_PATH="/home/ub2/GIT_REPOS/tesseract/java"
  ```


### [Leptonica](http://www.leptonica.org/download.html)
- [Leptonica: C-API Reference](http://tpgit.github.io/UnOfficialLeptDocs/leptonica/functions.html)
- ##### Install:
  ```bash
  ./configure
  make
  make install
  ```

### OpenCV
- [Examples](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials)
- [Doc Scanner In A Day: Part 1](http://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/)
- [Doc Scanner In A Day: Part 2](http://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/)


### ImageMagick
- [Positional Arg Clarity](http://www.imagemagick.org/discourse-server/viewtopic.php?t=18241)


### GUIs:
- [Paperwork](https://github.com/jflesch/paperwork)

 
### Command Line:
- `identify [-verbose]`
  - obtain detailed information and calculations (careful with verbose)


- `jpegtopnm`
  - "JPEG" a.k.a. "JFIF"
  - `-comments` prints any comments to stderr
  - `-exif=-` prints EXIF header to stdout (no image output)
  - `dumpexif`
  - OUTPUT format: 
    - PGM (Portable Graymap) [if INPUT is grayscale]
    - PPM (Portable Pixmap) [if INPUT is NOT grayscale]
    - either one byte or two bytes per sample depending on whether the JFIF input has either 8 bits or 12 bits per sample.
      - use `pnmdepth` for two-byte-per-sample --> one-byte-per-sample file if you need to.


- `wrjpgcom` - add comment to jpeg header


- `ppmdither`


- `pnmdepth` - one-byte-per-sample file most likely for raw PNM files pre-April 2000


- `cjpeg` - convert PPM,PGM,BMP,Targa,RLE to JPEG


- `jpegtran`


- `pgmtopbm` - Reads a portable graymap as input.  Produces a portable bitmap as output.


- `pgmhist`


- `pgmtofits`


- `pnmscale`


- `pnmtops`

- `pbmreduce`

- `pnmconvol`

- - - 


  ```bash
    pnmscale -xysize 2400 3000 image.pgm | pgmtopbm -hil | pnmtops -scale 0.25 > image.ps

    jpegtopnm \
      ~/ARCHIVE/DOC_IMAGES/test_orig.jpg \
      > ~/ARCHIVE/DOC_IMAGES/test_pnm.ppm
      
    ppmtopgm \
      ~/ARCHIVE/DOC_IMAGES/test_pnm.ppm|pgmtopbm \
      > ~/ARCHIVE/DOC_IMAGES/test_pnm_conv.pbm
      
    convert -deskew 40% test_pnm_conv_morphed.jpg \
      jpegtopnm - | pnmtotiff - | \
      tesseract - - pdf|pdftotext -layout - -
    
    convert -normalize -threshold 50% -brightness-contrast 0x10 in.JPG 1blackwhite.pbm
  ```



