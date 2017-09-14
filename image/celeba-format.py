# -*- coding: utf-8 -*-
"""
    @author: airylinus
    resize image to fix width/height
    can be used for image preprocessing before feed to caffe CNN
"""
# ----------------------------------------------------------------------------
import sys
import os
import cv2
import string
import numpy as np
from resizer import Resizer


def removeEmptyInList(list) :
    newList = [];
    for val in list :
        if val :
            newList.append(val);
    return newList;

def processImage(resizer, savePath, line):
    path = "/media/mongo/data/celeba-face/img_celeba/"
    scale = 1.0000

    f = path + line[0] 
    print "processing ... ", f
    img = cv2.imread(f)
    w = img.shape[1]
    h = img.shape[0]
    scaleBy = Resizer.scaleBy(w, h, resizer.width, resizer.height)
    print w, h, scaleBy
    if scaleBy == "x":
        scale = resizer.width * 1.0000 / w
    else :
        scale = resizer.height * 1.0000 / h
    dots = []
    print line[1:]
    for s in line[1:]:
        x = int(s) 
        dots.append(int(x * scale))
    newImg = resizer.resize(img)
    cv2.imwrite(savePath + line[0], newImg)
    n = 0
    labels = line[0]
    while(n < 5):
        idx = n * 2
        dot = (dots[idx], dots[idx + 1])
        # print dot
        # cv2.circle(newImg, (dots[idx], dots[idx+1]), 2, (55,255,155))
        labels += " " + str(dots[idx]) + " " + str(dots[idx+1]) + " 1"
        n += 1
    # print labels
    # cv2.imshow("xxx", newImg)
    # if cv2.waitKey() == 23:
    #     cv2.destroyAllWindows()
    return labels

if "__main__" == __name__:
    if len(sys.argv) != 3:
        print ""
        exit
    labelFile = sys.argv[1]
    savePath = sys.argv[2]
    destW = 400
    destH = 300
    resizer = Resizer(destW, destH)
    f = open(savePath + "label.txt", "w")

    for line in open(labelFile):
        line = line.rstrip()
        # print line.split(" ")
        l = removeEmptyInList(line.split(" "))
        label = processImage(resizer, savePath, l)
        f.write(label + "\r\n")
