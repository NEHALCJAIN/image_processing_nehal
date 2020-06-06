import cv2
import numpy

cap = cv2.VideoCapture(0)
count = 0
while True:
    count = count + 1
    x,red= cap.read()
    vertf1 = numpy.rot90(red)
    if (count % 2 == 0):
        cv2.imshow("img",vertf1)
    else:
        vertf2=cv2.flip(vertf1,-1)
        cv2.imshow("img",vertf2)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
