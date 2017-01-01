


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


    """

    def __init__(self,_parent,kwargs={}):
        self                                =   _parent.T.To_Sub_Classes(self,_parent)
        self.T                              =   _parent.T

    def get_page_num(self):
        return self.T.br.execute("return PDFViewerApplication.page;")
    def get_page_count(self):
        return self.T.br.execute("return PDFViewerApplication.pdfViewer.pagesCount;")
    
    def goto_page(self,pgnum):
        js =    """
                PDFViewerApplication.pdfViewer.currentPageNumber = %d;
                """ % pgnum
        self.T.br.execute(js)
    def goto_first_page(self):
        js =    """
                PDFViewerApplication.pdfViewer.currentPageNumber = 1;
                """
        self.T.br.execute(js)
    def goto_last_page(self):
        js =    """
                var last_page = PDFViewerApplication.pdfViewer.pagesCount;
                PDFViewerApplication.pdfViewer.currentPageNumber = last_page;
                """
        self.T.br.execute(js)
    def goto_prev_page(self):
        js =    """
                function goToPreviousPage() {
                    var page = PDFViewerApplication.pdfViewer.currentPageNumber;
                    // If we're at the first page, we don't need to do anything.
                    if (page <= 1) {
                        return false;
                    }
                    PDFViewerApplication.pdfViewer.currentPageNumber = page - 1;
                    return true;
                    };
                return goToPreviousPage();
                """
        self.T.br.execute(js)
    def goto_next_page(self):
        js =    """
                function goToNextPage() {
                    var page = PDFViewerApplication.pdfViewer.currentPageNumber;
                    // If we're at the first page, we don't need to do anything.
                    if (page >= PDFViewerApplication.pdfViewer.pagesCount) {
                        return false;
                    }
                    PDFViewerApplication.pdfViewer.currentPageNumber = page + 1;
                    return true;
                    };
                return goToNextPage();
                """
        self.T.br.execute(js)

    def get_metadata(self):
        return self.T.br.execute("return PDFViewerApplication.metadata;")
    def get_page_text_content(self,pgnum):
        return self.T.br.execute("return $(PDFViewerApplication.appConfig.viewerContainer).children()[%d].innerText;" % pgnum)
    def get_all_text_content(self):
        return self.T.br.execute("return PDFViewerApplication.pdfViewer.container.textContent;")
    def get_rotation(self):
        return self.T.br.execute("return PDFViewerApplication.pageRotation;")
    def set_rotation(self,rotation):
        """rotation degrees (0, 90, 180, 270)"""
        js =    """
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
                rotate_page(%d);
                """ % rotation
        self.T.br.execute(js)

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
