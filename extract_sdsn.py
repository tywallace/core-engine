# -*- coding: utf-8 -*-
"""
Extract text for each SDSN metatopic and save to json file
"""

from extract_text import TextExtractor
from sdsn_clusters import sdsnClusters
from extract_sdg import detectFormat, extractText, concatText, save2json


if __name__ == "__main__":
    metatopicDict = {metatopic: [] for metatopic in sdsnClusters.keys()}

    #append text to list values for each key in metatopicDict
    for key in sdsnClusters.keys():
        print key
        for url in sdsnClusters[key]:
            print url
            extractor = TextExtractor(url)
            extractor.getResponse()
            pdf = extractor.getResponse().openPdfResponse()
            pdf.minePdf()
            #extract text and append to dictionary
            metatopicDict[key].append(pdf.text)

    for key in metatopicDict.keys():
        text = concatText(metatopicDict[key])
        metatopicDict[key] = text

    save2json('data/sdsn.json', [metatopicDict])
