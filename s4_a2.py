import cv2
import numpy as np

img =cv2.imread('lena.jpg')
points=[]
def mouse(event,x,y,flags,param):

    if event==cv2.EVENT_LBUTTONDOWN:
        points.append((x,y))

        if len(points)==2:
            x1,y1=points[0]
            x2,y2=points[1]
            crop=img[points[0][1]:points[1][1],points[0][0]:points[1][0]]
            cv2.imshow("Cropped",crop)

cv2.namedWindow("copy")
cv2.setMouseCallback("copy",mouse)
cv2.imshow("copy",img)
cv2.waitKey(0)