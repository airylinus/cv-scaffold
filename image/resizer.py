# -*- coding: utf-8 -*-
"""
    @author: airylinus
    resize image to fix width/height
    can be used for image preprocessing before feed to caffe CNN
"""
# ----------------------------------------------------------------------------
import sys
import cv2
import numpy as np

class Resizer(object):
    # resize image to a fix width/height 
    
    def __init__(self, toWidth, toHeight):
        # final size wanted
        self.width = toWidth
        self.height = toHeight
    
    def resize(self, img):
        # img should be a image loaded by cv2.imread() 
        oWidth = img.shape[1]
        oHeight = img.shape[0]
        meanningWd, meanningHt = Resizer.scaleSize(oWidth, oHeight, self.width, self.height)
        meanningImg = cv2.resize(img, dsize=(meanningWd, meanningHt))
        print oWidth, oHeight
        print meanningWd, meanningHt
        image = Resizer.createRGB(self.width, self.height)
        image[0: meanningHt, 0: meanningWd] = meanningImg
        return image

    @staticmethod
    def scaleBy(fromWidth, fromHeight, toWidth, toHeight):
        # calculate useful size when scale by rate
        toRate = toHeight * 10000 / toWidth
        originRate = fromHeight * 10000 / fromWidth
        if originRate > toRate:
            return "y"
        return "x"

    @staticmethod
    def scaleSize(fromWidth, fromHeight, toWidth, toHeight):
        # calculate useful size when scale by rate
        scaleBy = Resizer.scaleBy(fromWidth, fromHeight, toWidth, toHeight)
        if scaleBy == "y":
            nx = fromWidth * 1.0 * toHeight / fromHeight
            return int(nx), toHeight
        else:
            ny = fromHeight * 1.0 * toWidth / fromWidth
            return toWidth, int(ny)
    
    @staticmethod
    def createRGB(width, height, r=104, g=117, b=123):
        # create new rbg image
        nImg = np.zeros((height, width, 3), np.uint8)
        nImg[:] = (r, g, b)
        return nImg

if "__main__" == __name__:
    if len(sys.argv) < 4:
        print "example :"
        print "            resize.py /path/to/image.jpg 400 300"
        print "            resize iamge.jpg to 400px width 300px height"
        exit(1)
    img = cv2.imread(sys.argv[1])
    resizer = Resizer(400, 300)
    nImg = resizer.resize(img)
    cv2.imshow("test", nImg)
    if cv2.waitKey() == 23:
        cv2.destroyAllWindows()