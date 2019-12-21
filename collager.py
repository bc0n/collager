#!/usr/bin/env python
# encoding: utf-8

# MIT License
# Copyright (c) 2019 Ben Conrad
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import glob
import cv2
import numpy
import sys
import re

def bakSum( bak, img ):
    mins = 1e11
    retr = 0
    retc = 0
    for itry in range(0,50):
        r = numpy.random.randint(0, padrow)
        c = numpy.random.randint(0, padcol)
        s = bak[r:(r+img.shape[0]),c:(c+img.shape[1])].sum()
        # print('r{}c{} = {} <? {}'.format(r,c,s, mins))
        if s < mins:
            mins = s
            retr = r
            retc = c
    return (retr,retc)

#default args
pdir = '.' #picture directory
overscale = 1
outcol = 1920*overscale #output video horizontal size
outrow = 1080*overscale #output video vertical size
secPerFrame = 10;
frac = 0.5 #size of an individaul picture relative to overall video size

print( sys.argv )

if  1 < len(sys.argv):
    pdir = sys.argv[1]
if  2 < len(sys.argv):
    outcol = int(sys.argv[2])
if  3 < len(sys.argv):
    outrow = int(sys.argv[3])
if  4 < len(sys.argv):
    secPerFrame = float(sys.argv[4])
if  5 < len(sys.argv):
    frac = float(sys.argv[5])

jpg = glob.glob('{}/*.jpg'.format(pdir))
JPG = glob.glob('{}/*.JPG'.format(pdir))
bmp = glob.glob('{}/*.bmp'.format(pdir))
BMP = glob.glob('{}/*.BMP'.format(pdir))
png = glob.glob('{}/*.png'.format(pdir))
PNG = glob.glob('{}/*.PNG'.format(pdir))
imgList = jpg + JPG + bmp + BMP + png + PNG

if len(imgList) == 0:
    print(sys.argv)
    print('collager.py stacks images found in the given directory into a slideshow.\nGiven insufficient arguments, use\n>>python collager.py directory width height secPerFrame pictureSizeFactor')
    exit()

print('>>python imageStacking.py {} {} {} {} {}'.format(pdir, outcol, outrow, secPerFrame, frac ))
print('Loading {} images from {}'.format(len(imgList), pdir))

imgList = sorted( imgList ) # default sort is alphabetical
# def getImageNumber(name):
#     mat = re.match( r'2019-JPG \(([0-9]*)', name )
#     return float(mat.group(1))
# imgList = sorted( glob.glob('*.jpg'), key=getImageNumber ) sort by regex-parsed filename

fps = float(1.0/secPerFrame)
subcol = outcol * frac
subrow = outrow * frac
padcol = outcol - subcol
padrow = outrow - subrow
print('resize: padrow{} padcol{}'.format( padrow, padcol ))
sr = float(subrow)/float(subcol)
print('resize: subrow{} subcol{} sr{}'.format( subrow, subcol, sr ))

#choose video encoder
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
vid = cv2.VideoWriter( 'collager.avi', fourcc,  fps, (outcol,outrow) )

cnv = numpy.zeros( (outrow, outcol, 3), dtype=numpy.uint8 )
bak = numpy.zeros( (outrow, outcol, 1), dtype=numpy.uint8 )
cnt = 0

allrow = numpy.arange( 0, padrow ) #permissible row shifts
allcol = numpy.arange( 0, padcol )
prerow = []
precol = []

for imgName in imgList:
    # if 50 < cnt:
        # break

    cnt = cnt+1

    img = cv2.imread(imgName)

    ar = float(img.shape[0])/float(img.shape[1]) #== rows / cols, portrait == rows > cols, ar > 1
    print('{} of {}: opened {} with size rows{},cols{},depth{},ar{}'.format( cnt, len(imgList), imgName, img.shape[0], img.shape[1], img.shape[2], ar ) )

    #if we resize the image to so that img.row == subrow, is imgcol > subcol, that subcol is limiting?
    limcol = round(subrow/ar);
    limrow = round(subcol*ar);
    # print('resizing: limrow{} limcol{}'.format(limrow,limcol))
    if ar < sr: #img is landscape
        # print('limited by row, resize to row{} col{} r{}'.format(limrow,subcol, limrow/subcol))
        img = cv2.resize( img, (int(subcol), int(limrow)) )
    else: #img is portrait
        # print('limited by col, resize to row{} col{} r{}'.format(subrow,limcol, subrow/limcol))
        img = cv2.resize( img, (int(limcol), int(subrow)) )

    r,c = bakSum( bak, img)

    cnv[int(r):int(r+img.shape[0]), int(c):int(c+img.shape[1])] = img
    bak[r:(r+img.shape[0]),c:(c+img.shape[1])] = numpy.add(bak[r:(r+img.shape[0]),c:(c+img.shape[1])], 1)

    prerow.append(r)
    precol.append(c)
    if 10 < len(prerow):
        prerow = prerow[ len(prerow)-10: ]
        precol = precol[ len(precol)-10: ]
    vid.write( cnv )

vid.write( cnv ) #rewrite last frame to ensure it isn't clipped
cv2.destroyAllWindows()
vid.release()



