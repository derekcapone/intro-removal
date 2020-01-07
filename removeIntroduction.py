import numpy
import cv2
import os

def generateFramePath(filename):
    path = os.getcwd()
    folder = "%s\%s_frames\\" % (path, filename)

    if(not generateDir(folder)):
        return False, ""
    else:
        return True, folder


def generateDir(path):
    if(not os.path.exists(path)):
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
            return(None)
        else:
            return(path)


vid1_name = "episode2.mp4"
vid2_name = "episode3.mp4"




# vidcap = cv2.VideoCapture('')
# success, image = vidcap.read()

# path = os.getcwd()
# print(path)

# for i in range(20):
#     cv2.imwrite("frame%d.jpg" % i, image)
#     success, image = vidcap.read()
#     print("reading frame %d" % i)



