import cv2
import numpy as np

img=cv2.imread('qwe.jpg')
pts=[]
def mouse(event,x,y,flags,param):
    if event==cv2.EVENT_LBUTTONDOWN:
        pts.append((x,y))
        print(pts)
    if len(pts)==4:
        pts1=np.array([pts[0],pts[1],pts[2],pts[3]],np.float32)
        pts2=np.array([(0,0),(500,0),(0,500),(500,500)],np.float32)
        persp=cv2.getPerspectiveTransform(pts1,pts2)
        trans=cv2.warpPerspective(img,persp,(500,500))
        cv2.imshow('new',trans)
cv2.namedWindow('img')
cv2.setMouseCallback('img',mouse)
cv2.imshow('img',img)
cv2.waitKey(0)