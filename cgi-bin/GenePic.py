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

        self.cursor.execute(""" select start,stop,rs_ID from TFBS left join RS on RS.TFBS_ID = TFBS.TFBS_ID where  TFBS.TFBS_ID = %d """ % (self.tfbs))
        row = self.cursor.fetchone()
        if row['rs_ID'] != None:
            hasSNP = 255
        else:
            hasSNP = 0
        self.features.append([int(row['start']), int(row['stop']), self.tfbs, hasSNP])

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

        # calculate SVG height
        prev = list()
        maxheight = 0
        for f in self.features:

            start  = self.__class__.sidemargin + float(f[0] - self.genestart) / float(self.geneend - self.genestart) * (100.0 - 2.0 * self.__class__.sidemargin)
            length = self.__class__.sidemargin + float(f[1] - self.genestart) / float(self.geneend - self.genestart) * (100.0 - 2.0 * self.__class__.sidemargin) - start
            length = max(length, 0.5)
            height = 0 # it is not a percentage, but the count

            for p in prev:
                if p[0] + p[1] > start and p[0] < start + length:
                    height += 1

            if height > maxheight:
                maxheight = height

            prev.append([start, length, height, f[2], f[3]])

        height  = self.__class__.tfbsheight * maxheight + 2 * self.__class__.topmargin
        counter = float(self.__class__.topmargin)  / float(height) * 100.0
        step    = float(self.__class__.tfbsheight) / float(height) * 100.0

        print('<svg id="tfbsimage" height="%d" width="70%%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">' % (height))
        print('<rect stroke="black" fill="none" x="0%" y="0%" width="100%" height="100%" />') # draw frame around picture

        # draw ruler
        print('<line x1="%f%%" y1="%f%%" x2="%f%%" y2="%f%%" stroke-width="1" stroke="black" />' % (self.__class__.sidemargin, 1.0, 100.0 - self.__class__.sidemargin, 1.0))
        for f in prev:
            start = f[0]
            width = f[1]
            ypos  = counter + step * f[2]
            print('<rect x="%.4f%%" y="%.4f%%" width="%.4f%%" height="%.4f%%" style="fill:rgb(%d,0,0)" onmouseover="this.style.stroke=\'#ff0000\'" title="tfbs%s" onmouseout="this.style.stroke=\'#000000\'" onclick="$(window).scrollTop($(\'#tfbs%s\').position().top)" />' % (start, ypos, width, step, f[4], f[3], f[3]))

        print("</svg>")
