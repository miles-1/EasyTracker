import sys
import cv2
from PIL import Image
import numpy as np


video = cv2.VideoCapture('/Users/miles/Desktop/test.mp4')
indx = 0
lastIndx = 0
imageDict = {}
diffDict = {}

success, current1 = False, None
while not success:
    success, current1 = video.read()

imageDict[indx] = current1

fps = video.get(cv2.CAP_PROP_FPS)
length = video.get(cv2.CAP_PROP_FRAME_COUNT)

print(fps,length)

while success:
    success, current2 = video.read()
    indx += 1
    if not success:
        break
    if (current1 != current2).any():
        imageDict[indx] = current2
        diffDict[lastIndx] = cv2.subtract(current1, current2)
        current1 = current2
        lastIndx = indx

print("NEXT")
thresh = 10

thing = Image.fromarray(diffDict[53]) #.convert("L") #.point(fn, mode='1')
thing.show()
thing = Image.fromarray(imageDict[53]) #.convert("L") #.point(fn, mode='1')
thing.show()
# for item, info in diffDict.items():
#     if item < 60:
#         thing = Image.fromarray(info[0])
#         thing.show()

