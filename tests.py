# -*- coding: utf-8 -*-

from extract_text import TextExtractor


print 'Running TextExtractor Test'

#### Docx test ####
url = 'http://sustainabledevelopment.un.org/getWSDoc.php?id=1349'
extractor = TextExtractor(url)
extractor.getResponse().openDocxResponse().getDocxText()
try: 
    isinstance(extractor.text, unicode)
    print "Docx successfully extracted"
except:
    print "Docx extraction unsuccessful"

#### Pdf test ####
url = 'http://sustainabledevelopment.un.org/getWSDoc.php?id=3310'
extractor = TextExtractor(url)
pdf = extractor.getResponse().openPdfResponse()
extractor.getPdfText()
try: 
    isinstance(extractor.text, unicode)
    print "Pdf successfully extracted"
except:
    print "Pdf extraction unsuccessful"

# for page in pdf.pages:
#     print page.extractText().encode('utf-8')
#print getPdfText(pdf).encode('utf-8')