from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import StringIO


class Miner(object):
    '''pdf extractor that only supports scraping url responses'''

    def __init__(self, urlContent, codec='utf-8'):
        self.fp = StringIO.StringIO()
        self.fp.write(urlContent)
        self.fp.seek(0)

        self.rsrcmgr = PDFResourceManager()
        self.retstr = StringIO.StringIO()
        self.laparams = LAParams()
        self.device = TextConverter(
            self.rsrcmgr, self.retstr, codec=codec, laparams=self.laparams)
        self.interpreter = PDFPageInterpreter(self.rsrcmgr, self.device)

    def extract_text(self, password="", maxpages=0, caching=True, pagenos=set()):
        for page in PDFPage.get_pages(self.fp, pagenos,
                                      maxpages=maxpages,
                                      password=password,
                                      caching=caching,
                                      check_extractable=True):
            self.interpreter.process_page(page)
        self.fp.close()
        self.device.close()
        text = self.retstr.getvalue()
        self.retstr.close()
        return text