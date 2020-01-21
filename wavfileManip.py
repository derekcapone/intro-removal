import numpy as np
from scipy.io import wavfile
import scipy.signal as sig
import subprocess
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt 
import datetime


def printTimeDifference(t1, t2):
    """
    Prints time difference between two datetime objects in seconds
    t1 and t2 are datetime objects
    """
    duration = t2 - t1
    print("Time = %f" % duration.total_seconds())


def testWavWrite(filename, sampleRate, arr):
    wavfile.write(filename, sampleRate, arr)


def generateWavFiles(videos, path):
    """
    Generates wav files from each video title
    param: videos - list of video names to generate audio
    param: path - folder holding the videos
    """
    ffmpegPath = "C:/Users/derek/Downloads/ffmpeg-20200110-3d894db-win64-static/ffmpeg-20200110-3d894db-win64-static/bin/"
    count = 0

    for video in mp4_files:
        print("Generating audio for %s" % video)
        abs_video = path + "/" + video
        print(abs_video)
        wavtitle = "audiotracks/track%d.wav" % count  # create audio file name
        command = "%s/ffmpeg.exe -i %s -ab 160k -ac 2 -ar 44100 -vn %s -y" % (ffmpegPath, abs_video, wavtitle)  # generate wav file
        subprocess.call(command, shell=True)  # execute ffmpeg command
        count += 1


def getVideoFiles(path):
    """
    Creates a list of .mp4 video files for the given directory path
    """
    mp4_files = []
    for f in listdir(path):
        if(isfile(join(path, f)) and (f[-4:] == ".mp4" or f[-4:] == ".avi")):
            mp4_files.append(f)
    return mp4_files


def normalize(data):
    return data / np.linalg.norm(data)


def correlateArrays():
    fs1, samps1 = wavfile.read("audiotracks/track0.wav")
    fs2, samps2 = wavfile.read("audiotracks/track1.wav")
    data1 = np.array(samps1[:, 0])
    data2 = np.array(samps2[:, 0])

    # normalize and downsample signals
    five_mins = 13230000
    norm1 = data1[0:five_mins]
    norm2 = data2[0:five_mins]
    norm1 = normalize(norm1)
    norm2 = normalize(norm2)
    
    print(norm1.shape)

    # downsample data
    down1 = sig.decimate(norm1, 10)
    down2 = sig.decimate(norm2, 10)
    
    print(down1.shape)

    bb = 10000
    samples = down1.shape
    corr = np.zeros(samples)
    max = 0
    index = 0

    for fb in range(samples[0]):
        # correlate normalized arrays
        val = np.correlate(down1[fb:bb+fb], down2[fb:bb+fb])
        corr[fb] = val #np.append(corr, [val])
        print(fb)
        
        if(val > max):
            index = fb
            max = val
    
    print("max = %f" % max)
    print("index = %d" % index)
    
    
    


if __name__ == "__main__":
    # path = "C:/Users/derek/Videos/TVShows/TheSimpsons/Season06"
    # mp4_files = getVideoFiles(path)
    # generateWavFiles(mp4_files, path)

    correlateArrays()
    
