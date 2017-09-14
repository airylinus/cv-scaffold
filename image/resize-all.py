import glob
import cv2
import os
import sys
from resizer import Resizer

if "__main__" == __name__:
    if len(sys.argv) != 5:
        print "example :"
        print "            resize.py /path/to/image.jpg 400 300 /path/to/save/"
        print "            resize iamge.jpg to 400px width 300px height"
        exit(1)
    imgDir = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    imgSaved = sys.argv[4]
    resizer = Resizer(width, height)
    for f in glob.glob(os.path.join(imgDir, "*.jpg")):
        print(f)
        name = f.split("/")[-1]
        img = cv2.imread(f)
        nImg = resizer.resize(img)
        cv2.imshow("test", nImg)
        
        if cv2.waitKey() == 23:
            cv2.destroyAllWindows()