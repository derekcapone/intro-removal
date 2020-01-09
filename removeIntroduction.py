import numpy
import cv2
import os
import shutil
import datetime
import pictureDifference

def generateFramePath(filename):
    path = os.getcwd()
    filename = filename.replace('.', '_')
    folder = "%s\%s_frames\\" % (path, filename)

    if(os.path.exists(folder)):
        shutil.rmtree(folder)  # remove folder

    if(not generateDir(folder)): 
        return False, ""
    else:
        return True, folder


def generateDir(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
        return(None)
    else:
        return(path)


def getFPS(vidcap):
    return vidcap.get(cv2.CAP_PROP_FPS)


def printTimeDifference(t1, t2):
    """
    Prints time difference between two datetime objects in seconds
    t1 and t2 are datetime objects
    """
    duration = t2 - t1
    print("Time = %f" % duration.total_seconds())


vid1_name = "episode2.mp4"
success1, folder1 = generateFramePath(vid1_name)

# catch errors with directory creation
if(not success1):
    print("Frame directory creation error")
    exit()

vidcap = cv2.VideoCapture(vid1_name)
succ1, image1 = vidcap.read()

frame_path = folder1 + "frame00.jpg"
cv2.imwrite(frame_path, image1)

succ1, image = vidcap.read()

for i in range(200):
    frame_path = folder1 + "frame%d.jpg" % i  # generate the absolute path for each frame
    cv2.imwrite(frame_path, image)
    success, image = vidcap.read()

    mse_val = pictureDifference.mse(image1, image)
    print("Frame %d: %f" % (i, mse_val))

