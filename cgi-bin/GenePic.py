#!/usr/bin/env python3

class GenePic:
    def __init__(self):
        self.genes = dict()
    def add(self, genename, tfbsstart, tfbsend, genestart):
        if genename not in self.genes:
            self.genes[genename] = list()
        relativestart = int(tfbsstart) - int(genestart)
        relativeend   = int(tfbsend) - int(genestart)
        self.genes[genename].append([relativestart, relativeend])
    def drawpic():
        print('<svg id="tfbsimage" height="60" width="60" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">')
        print("</svg>")

