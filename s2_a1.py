import cv2
img=cv2.imread('good.jpg')
print(img.shape)
cv2.line(img,(0,0),(792,1056),(0,0,0),5)
cv2.imshow('win',img)
cv2.waitKey(0)