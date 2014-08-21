# -*- coding: utf-8 -*-
"""
Extract text from pdf and docx files

Source Code Adapted from: https://github.com/mikemaccana/python-docx
"""

import urllib2
import zipfile
from StringIO import StringIO
from lxml import etree


# All Word prefixes / namespace matches used in document.xml & core.xml.
# LXML doesn't actually use prefixes (just the real namespace) , but these
# make it easier to copy Word output more easily.
nsprefixes = {
    'w':   'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    }


def getDocxResponse(url):
    response = urllib2.urlopen(url)
    return response.read()


def openDocxResponse(content):
    fp = StringIO(content)
    zfp = zipfile.ZipFile(fp, 'r')
    xmlContent = zfp.read('word/document.xml')
    document = etree.fromstring(xmlContent)
    return document


def getDocumentText(document):
    '''Return the raw text of a document as a list of paragraphs.'''
    paratextlist = []
    # Compile a list of all paragraph (p) elements
    paralist = [e for e in document.iter()
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
    return paratextlist


url = 'http://sustainabledevelopment.un.org/getWSDoc.php?id=1349'
urlContent = getDocxResponse(url)
document = openDocxResponse(urlContent)
text = getDocumentText(document)
print ' '.join(text).encode('utf-8')
