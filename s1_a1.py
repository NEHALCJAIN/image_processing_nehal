import cv2
cap=cv2.VideoCapture(0)
count=0
while True:
    x,red=cap.read()
    count+=1
    if count%5==0:
        flipped=cv2.flip(red,-1)
        cv2.imshow('win',flipped)
    else:
        cv2.imshow('win',red)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break