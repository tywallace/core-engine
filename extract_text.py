# -*- coding: utf-8 -*-
"""
Extract text from pdf and docx files

Source Code Adapted from: https://github.com/mikemaccana/python-docx
"""

import urllib2
import zipfile
from StringIO import StringIO
from lxml import etree
from PyPDF2 import PdfFileReader
from miner import Miner
import re

# All Word prefixes / namespace matches used in document.xml & core.xml.
# LXML doesn't actually use prefixes (just the real namespace) , but these
# make it easier to copy Word output more easily.
nsprefixes = {
    'w':   'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    }


class TextExtractor(object):

    def __init__(self, url, fileFormat=None):
        self.url = url
        self.fileFormat = fileFormat

    def getResponse(self):
        self.response = urllib2.urlopen(self.url)
        self.content = self.response.read()
        return self

    def openDocxResponse(self):
        fp = StringIO(self.content)
        zfp = zipfile.ZipFile(fp, 'r')
        xmlContent = zfp.read('word/document.xml')
        self.document = etree.fromstring(xmlContent)
        return self

    def openPdfResponse(self):
        self.fp = StringIO(self.content)
        self.document = PdfFileReader(self.fp)
        return self

    def getDocxText(self):
        '''Return the raw text of a document as a list of paragraphs.'''
        paratextlist = []

        # Compile a list of all paragraph (p) elements
        paralist = [e for e in self.document.iter()
                    if e.tag == '{' + nsprefixes['w'] + '}p']

        # Since a single sentence might be spread over multiple text elements,
        # iterate through each paragraph, appending all text (t) children to that
        # paragraphs text.
        for para in paralist:
            paratext = u''
            # Loop through each paragraph
            for element in para.iter():
                # Find t (text) elements
                if element.tag == '{' + nsprefixes['w'] + '}t' and element.text:
                    paratext = paratext + element.text
                elif element.tag == '{' + nsprefixes['w'] + '}tab':
                    paratext = paratext + '\t'
            # Add our completed paragraph text to the list of paragraph text
            if not len(paratext) == 0:
                paratextlist.append(paratext)

        self.text = ' '.join(paratextlist)
        return self

    def getPdfText(self):
        '''Return the raw text of a pdf file'''
        pdf = self.document.pages
        self.text = ' '.join([p.extractText() for p in pdf])
        return self

    def getText(self):
        '''Conditional wrapper for getDocxText and getPdfText'''
        if self.fileFormat == 'pdf':
            self.getPdfText()
        elif self.fileFormat == 'docx':
            self.getDocxText()
        else:
            self.text = ''


if __name__ == "__main__":

    #### Docx test ####
    # url = 'http://sustainabledevelopment.un.org/getWSDoc.php?id=1349'
    # extractor = TextExtractor(url)
    # document = extractor.getResponse().openDocxResponse()
    # text = extractor.getDocxText()
    # print extractor.text.encode('utf-8')

    #### Pdf test ####
    # url = 'http://sustainabledevelopment.un.org/getWSDoc.php?id=3310'
    url = 'http://unsdsn.org/wp-content/uploads/2014/02/Health-For-All-Report.pdf'
    extractor = TextExtractor(url)
    pdf = extractor.getResponse().openPdfResponse()
    miner = Miner(pdf.content)
    text = miner.extract_text()
    print text.split()[:100]
    cleanText = ' '.join(text.split())
    print cleanText.decode('utf8').encode('ascii', 'ignore')
    # file(pdf.content, 'rb')

    #print extractor.text.encode('utf-8')

    # for page in pdf.pages:
    #     print page.extractText().encode('utf-8')
    #print getPdfText(pdf).encode('utf-8')