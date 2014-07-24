#!/usr/bin/env python3

import MySQLdb as mdb

class GenePic:

    tfbsheight = 10             # height of the features in pixel
    topmargin  = 5              # top and bottom margin in pixel
    sidemargin = 5.0            # left and right margin in percentage

    def __init__(self,geneid):
        self.geneid    = geneid
        self.tfbs      = list()
        self.features  = list()
        self.cursor    = None
        self.genestart = 0
        self.geneend   = 0

    # add a list of tfbs ids
    def addTFBS(self, tfbs):
        self.tfbs = tfbs
        if self.cursor == None:
            raise Exception("Cursor not set!")

        self.cursor.execute(""" select start,stop from TFBS where TFBS_ID = %d """ % (self.tfbs))
        row = self.cursor.fetchone()
        self.features.append([int(row['start']), int(row['stop'])])

    # set cursor for database queries
    def setcursor(self, cur):
        self.cursor = cur

    # finally draw some pictures
    def drawpic(self):
        if self.cursor == None:
            raise Exception("Cursor not set!")

        # get the start and end coordinates of the gene
        self.cursor.execute(""" select start,end from GENE where gene_id = %s""" % (self.geneid))
        row = self.cursor.fetchone()
        self.genestart = int(row['start'])
        self.geneend   = int(row['end'])

        # SVG drawing code
        print('<br />')

        height  = self.__class__.tfbsheight * len(self.features) + 2 * self.__class__.topmargin
        counter = float(self.__class__.topmargin)  / float(height) * 100.0
        step    = float(self.__class__.tfbsheight) / float(height) * 100.0

        print('<svg id="tfbsimage" height="%d" width="70%%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">' % (height))
        print('<rect stroke="black" fill="none" x="0%" y="0%" width="100%" height="100%" />') # draw frame around picture

        # draw ruler
        print('<line x1="%f%%" y1="%f%%" x2="%f%%" y2="%f%%" stroke-width="1" stroke="black" />' % (self.__class__.sidemargin, 1.0, 100.0 - self.__class__.sidemargin, 1.0))

        for f in self.features:

            start = self.__class__.sidemargin + float(f[0] - self.genestart) / float(self.geneend - self.genestart) * (100.0 - 2.0 * self.__class__.sidemargin)
            end   = self.__class__.sidemargin + float(f[1] - self.genestart) / float(self.geneend - self.genestart) * (100.0 - 2.0 * self.__class__.sidemargin) - start
            end   = max(end, 0.5)

            print('<rect x="%f%%" y="%f%%" width="%f%%" height="%f%%" />' % (start, counter, end, step))

            counter += step

        print("</svg>")
