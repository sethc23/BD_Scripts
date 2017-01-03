


class PDF_Viewer:

    """
    PDFViewerApplication\
        - [X] .pageRotation
        - [X] .pagesCount
        - [X] .page_content PAGES
        - [X] .metadata
        - [X] .rotatePages PAGES
        - [X] .hasPageLabels

        - [X] SCROLL UP/DOWN
        - [X] FIRST/LAST PAGE
        - [X] NEXT/PREV PAGE
        - [] NEXT/PREV DOC

            'q'         : 'quit',
            'm'         : 'mark file (append filepath to save file)',
            'P'         : 'goto previous file',
            'N'         : 'goto next file',
            'p'         : 'goto previous page in file',
            'n'         : 'goto next page in file',
            'f'         : 'goto first page of file',
            'e'         : 'goto last page of file',
            'L'         : 'rotate 90 left (counter-clockwise)',
            'R'         : 'rotate 90 right (clockwise)',
            '?'         : 'show info about file and update query',
            'o'         : 'print OCR of file',
            'D'         : 'execute update query and goto next file',

            're [str]'  : 'test,save,edit,remove regex queries re: OCR text',
            '! [str]'   : 'execute ipython command in this namespace',
            'j [int]'   : 'jump to file having input uid',


        PDFViewerApplication.pdfViewer.eventBus.dispatch('rotatecw')
        this.eventBus.dispatch('rotatecw')
        this.eventBus.dispatch('firstpage');
        .getPage()
        .getPageTextContent()
        PDFViewerApplication.pdfViewer._getVisiblePages().views["0"].view.textLayer.textLayerRenderTask._textContent

    """

    def __init__(self,_parent,kwargs={}):
        self                                =   _parent.T.To_Sub_Classes(self,_parent)
        self.T                              =   _parent.T


    def get_page_path(self):
        return self.T.br.execute("return window.location.pathname;").lstrip('/')
    def get_page_num(self):
        return self.T.br.execute("return PDFViewerApplication.page;")
    def get_page_count(self):
        return self.T.br.execute("return PDFViewerApplication.pdfViewer.pagesCount;")

    def goto_page(self,pgnum):
        js =    """
                PDFViewerApplication.pdfViewer.currentPageNumber = %d;
                return PDFViewerApplication.page;
                """ % pgnum
        return self.T.br.execute(js)
    def goto_first_page(self):
        js =    """
                PDFViewerApplication.pdfViewer.currentPageNumber = 1;
                return PDFViewerApplication.page;
                """
        return self.T.br.execute(js)
    def goto_last_page(self):
        js =    """
                var last_page = PDFViewerApplication.pdfViewer.pagesCount;
                PDFViewerApplication.pdfViewer.currentPageNumber = last_page;
                return PDFViewerApplication.page;
                """
        return self.T.br.execute(js)
    def goto_prev_page(self):
        js =    """
                function goToPreviousPage() {
                    var page = PDFViewerApplication.pdfViewer.currentPageNumber;
                    // If we're at the first page, we don't need to do anything.
                    if (page <= 1) {
                        return page;
                    }
                    page -= 1;
                    PDFViewerApplication.pdfViewer.currentPageNumber = page;
                    return page;
                    };
                return goToPreviousPage();
                """
        return self.T.br.execute(js)
    def goto_next_page(self):
        js =    """
                function goToNextPage() {
                    var page = PDFViewerApplication.pdfViewer.currentPageNumber;
                    // If we're at the first page, we don't need to do anything.
                    if (page >= PDFViewerApplication.pdfViewer.pagesCount) {
                        return page;
                    }
                    page += 1;
                    PDFViewerApplication.pdfViewer.currentPageNumber = page + 1;
                    return page;
                    };
                return goToNextPage();
                """
        return self.T.br.execute(js)

    def get_metadata(self):
        return self.T.br.execute("return PDFViewerApplication.metadata;")
    def get_page_text_content(self,pgnum=0):
        if pgnum==0:
            pgnum = get_page_num()
        js  =   """
                function extractPageText(pageIndex) {
                    PDFViewerApplication.pdfViewer.getPageTextContent(pageIndex).then(function textContentResolved(textContent) {
                        var textItems = textContent.items;
                        var str = [];
                        for (var i = 0, len = textItems.length; i < len; i++) {
                            str.push(textItems[i].str);
                        }
                        // Store the pageContent as a string.
                        res.push(str.join(''));
                        if (pageIndex + 1 < PDFViewerApplication.pdfViewer.pagesCount) {
                            extractPageText(pageIndex + 1);
                        }
                    });
                    }
                extractPageText(31)
                """
        return self.T.br.execute("return $(PDFViewerApplication.appConfig.viewerContainer).children()[%d].innerText;" % pgnum)
    def get_all_text_content(self):
        return self.T.br.execute("return PDFViewerApplication.pdfViewer.container.textContent;")
    def get_rotation(self):
        return self.T.br.execute("return PDFViewerApplication.pdfViewer._pagesRotation;")
    def set_rotation(self,rotation):
        """rotation degrees (0, 90, 180, 270)"""

        if hasattr(self.T,'re'):
            re = self.T.re
        else:
            import re

        if type(rotation)==int or rotation.isdigit():
            rotation                    =   rotation if type(rotation)==int else int(rotation)
        else:
            if re.search('right|cw|clock[-]?wise',rotation.lower()):
                rotate                  =   'cw'
            elif re.search('left|ccw|counter[-]?clock',rotation.lower()):
                rotate                  =   'ccw'
            else:
                print('Unknown value for param "rotation"')
                raise SystemError
            current                     =   self.get_rotation()
            rotation                    =   current + 90 if rotate=='cw' else current - 90

        # reduce to comparable value, where value<=360
        rotation                        =   rotation - ( 360 * (rotation/360) )
        # reduce to closest increment of 90
        rotation                        =   90 * int(round(rotation/90.0))

        js =    '\n'.join([
                            """
                            function rotate_page(rotation) {
                                if (!(typeof rotation === 'number' && rotation % 90 === 0)) {
                                    throw new Error('Invalid pages rotation angle.');
                                }
                                PDFViewerApplication.pdfViewer._pagesRotation = rotation;
                                if (!PDFViewerApplication.pdfViewer.pdfDocument) {
                                    return;
                                }
                                for (var i = 0, l = PDFViewerApplication.pdfViewer._pages.length; i < l; i++) {
                                    var pageView = PDFViewerApplication.pdfViewer._pages[i];
                                    pageView.update(pageView.scale, rotation);
                                }
                                PDFViewerApplication.pdfViewer._setScale(PDFViewerApplication.pdfViewer._currentScaleValue, true);
                                if (PDFViewerApplication.pdfViewer.defaultRenderingQueue) {
                                    PDFViewerApplication.pdfViewer.update();
                                }
                                };
                            """
                            ,"rotate_page(%d);" % rotation
                            ])
        self.T.br.execute(js)
        return rotation

    def scroll_page(self,direction='down'):
        direction_num = 1 if direction=='down' else -1
        js =    """
                var _window = PDFViewerApplication.pdfViewer.container;
                var doc_height = _window.getBoundingClientRect()['height'];
                var scrollPercent = 0.75;
                var scroll_amount = Math.round( scrollPercent * doc_height );
                _window.scrollBy( 0, scroll_amount * %d );
                """ % direction_num
        self.T.br.execute(js)
