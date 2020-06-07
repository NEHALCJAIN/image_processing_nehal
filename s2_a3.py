import cv2
import time
cam=cv2.VideoCapture(0)
start=time.time()
end=time.time()
while True:
    x,red=cv2.read()
    if end-start==5:
        flipped=cam.flip(red,-1)
        cv2.imshow('win',flipped)
    else:
        cv2.imshow('win',red)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
