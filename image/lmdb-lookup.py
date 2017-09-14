#import caffe
import lmdb
import PIL.Image
from StringIO import StringIO
import numpy as np
import sys
import os
import matplotlib.pyplot as plt


sys.path.insert(0, '/home/mongo/ml-workspace/caffe/projects/caffe-1.0/python/')

import caffe
print caffe.__version__

def read_lmdb(lmdb_file):
    cursor = lmdb.open(lmdb_file, readonly=True).begin().cursor()
    datum = caffe.proto.caffe_pb2.Datum()
    for _, value in cursor:
        datum.ParseFromString(value)
        s = StringIO()
        s.write(datum.data)
        s.seek(0)

        yield np.array(PIL.Image.open(s)), datum.label

def read_images_from_lmdb(db_path) :
    
    """
    Loops over image data in the lmdb, and displays information about each datum
    Assumes that data dimensions are as follows: (channels, height, width)
    """
    ax = plt.subplot(111)
    plt.hold(False)
    lmdb_env = lmdb.open(db_path, readonly=True)    
    with lmdb_env.begin() as lmdb_txn :
        lmdb_cursor = lmdb_txn.cursor() 
        #for it in lmdb_cursor.iternext() :
        while lmdb_cursor.next() :
            value = lmdb_cursor.value()
            key = lmdb_cursor.key()
            
            datum = caffe.proto.caffe_pb2.Datum()
            datum.ParseFromString(value)
            image = np.zeros((datum.channels, datum.height, datum.width))
            image = caffe.io.datum_to_array(datum)   
            image = np.transpose(image, (1, 2, 0))    # -> height, width, channels
            image = image[:,:,::-1]                   # BGR -> RGB
              
            print("key: ", key)
            print('label: {}'.format(datum.kps))
            print("image shape: " + str(image.shape) + ", data type: " + str(image.dtype) + ", random pixel value: " +  str(image[150,150,0]))
                        
            ax.imshow(np.squeeze(image))
            plt.draw()
            plt.waitforbuttonpress()
            
    plt.show() 
    lmdb_txn.abort()
    lmdb_env.close()

    return


if "__main__" == __name__:
    db_path = sys.argv[1]
    if not os.path.exists(db_path):
        raise Exception('db path not found : ' + db_path)
    read_images_from_lmdb(db_path)
        
    #for im, label in read_lmdb(lmdb_dir):
    #    print label, im
