# -*- coding: utf-8 -*-
"""
Extract text for each SDG metatopic and save to json file
"""

from extract_text import TextExtractor
from sdg_clusters import sdgClusters
import json


def detectFormat(extractor):
    '''
    Takes an extractor object and tries to detect response.
    If response detected, opens url response for text extraction
    '''
    # tries opening url response as pdf
    # if there is an error, defers to
    # opening url response as docx

    formatDetected = False

    try:
        extractor.openPdfResponse()
        extractor.fileFormat = 'pdf'
        print 'pdf detected, fetching response'
        formatDetected = True
    except:
        print 'pdf not detected, attempting to open as docx'

    # if formatDetected is still false,
    # attempt to open url response as docx
    if formatDetected is False:
        try:
            extractor.openDocxResponse()
            extractor.fileFormat = 'docx'
            print 'docx detected, fetching response'
        except:
            print 'file format not detected, text cannot be extracted'

    return extractor


def extractText(extractor):
    extractor.getText()
    return extractor.text


def concatText(textList):
    return ' '.join(textList)


def save2json(filePath, dictObj):
    #saves dictionery object to specified json file
    with open(filePath, 'w') as f:
        json.dump(dictObj, f)


if __name__ == "__main__":

    # define a metatopic dictionary
    metatopicDict = {metatopic: [] for metatopic in sdgClusters.keys()}

    #append text to list values for each key in metatopicDict
    for key in sdgClusters.keys():
        print key
        for url in sdgClusters[key]:
            print url
            extractor = TextExtractor(url)
            extractor.getResponse()
            detectFormat(extractor)
            #extract text and append to dictionary
            metatopicDict[key].append(extractText(extractor))

    for key in metatopicDict.keys():
        text = concatText(metatopicDict[key])
        metatopicDict[key] = text

    save2json('data/sdg.json', [metatopicDict])