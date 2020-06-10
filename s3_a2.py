import cv2
import random
img=cv2.imread('good1.jpg')
sha=img.shape
x=sha[1]/7
y=sha[0]/7
for ab in range(1,8):
    Sta1=int(y*(ab-1))
    En1=int(y*ab)
    if y%2==0:
        sta=1
        en=8
        step=1
    elif y%2!= 0:
        sta=7
        en=0
        step= -1
    for ac in range(sta,en,step):
        Sta2=int(x*(ac-1))
        En2=int(x*ac)
        img[Sta1:En1,Sta2:En2]=(random.randint(0,255),random.randint(0,255),random.randint (0,255))
        cv2.imshow('win',img)
        cv2.waitKey(300)
cv2.waitKey (1000)