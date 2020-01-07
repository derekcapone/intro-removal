import cv2

vidcap = cv2.VideoCapture('episode2.mp4')
success, image = vidcap.read()

for i in range(20):
    cv2.imwrite("frame%d.jpg" % i, image)
    success, image = vidcap.read()
    print("reading frame %d" % i)

