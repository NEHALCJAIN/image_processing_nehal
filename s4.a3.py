import cv2
import numpy as np


img = cv2.imread('qwe.jpg')
cv2.imshow('Frame',img)
pt=[(203,92),(1054,157),(1216,601),(268,714)]
pt1=[(0,0),(1080,0),(0,720),(1080,720)]
def m_event(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,y)


cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', m_event)

transform = cv2.getPerspectiveTransform(pt, pt1)
last= cv2.warpPerspective(img, transform, (720, 1080))


cv2.imshow('Frame', img)
cv2.imshow('Warpped', last)
cv2.waitKey(0)