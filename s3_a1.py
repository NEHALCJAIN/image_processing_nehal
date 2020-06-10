import cv2
import numpy as np
import random
img=cv2.imread ('good1.jpg')
sha=img.shape
y=sha[0] / 7
x=sha[1] / 7
for ab in range(1,8):
    St=int(x*(ab-1))
    En=int(x*ab)
    for ac in range(1,8):
        St=int(y*(ac-1))
        En=int(y*ac)
        img[St:En,St:En] = (random.randint (0, 255), random.randint (0, 255), random.randint (0, 255))
cv2.imshow ('win',img)
cv2.waitKey (1000)