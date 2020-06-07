import cv2
vid= cv2.VideoCapture (0)
count = 1
pathFormat ='E:\internship\session2\web_img\IMG_{0}.jpg'
while count<=100:
    x,img=vid.read()
    path=pathFormat.format(count)
    cv2.imwrite(path,img)
    count+=1
print(x)
