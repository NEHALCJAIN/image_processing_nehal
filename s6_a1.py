import cv2
import numpy as np
img=cv2.imread('lena.jpg')
img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

kernel = np.ones((25,25))

dilate = cv2.dilate(img_gray,kernel)

canny = cv2.Canny(dilate,50,250)
cv2.namedWindow ('canny', cv2.WINDOW_NORMAL)
cv2.namedWindow ('dilate', cv2.WINDOW_NORMAL)
cv2.namedWindow ('OG', cv2.WINDOW_NORMAL)
cv2.imshow("dilate",dilate)
cv2.imshow("canny",canny)
cv2.imshow ('OG', img_gray)
cv2.waitKey(0)