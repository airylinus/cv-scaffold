#!/usr/bin/env python

"""
Classifier is an image classifier specialization of Net.
"""

import cv2
import caffe
import sys


caffe.set_mode_gpu()


def binarinize_img(img):
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return th3


def with_net():
    pass


def with_classifier(mf, tf, lf, image_file):
    p = caffe.Classifier(mf, tf,
            channel_swap=(2, 1, 0), 
            raw_scale=255, 
            image_dims=(48, 48))
    input_image = caffe.io.load_image(image_file)
    output = p.predict([input_image])
    predictions = output[0]
    print(predictions.argmax())
    pi = predictions.argmax()
    labels = read_labels(image_file)
    print(len(labels))
    print(labels[predictions.argmax()])
    #labels = np.loadtxt(lf, str, delimiter='\t')
    #print('output label:', labels[predictions.argmax()])


def read_labels(label_file):
    f = open(label_file, "rb")
    data = f.read().splitlines()
    return data


if __name__ == "__main__":
    single_image = sys.argv[1]
    model_file = "./modelZSK/deploy.prototxt"
    trained_file = "./modelZSK/squeeze_zskV5_2765.caffemodel"
    label_file = "./modelZSK/alphabetzsk.txt"
    #labels = np.loadtxt(label_file, str, delimiter='\t')
    label_alphabets = "./models/chn_8300_split.txt"
    with_classifier(model_file, trained_file, label_file, single_image)
