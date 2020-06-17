import cv2
import numpy as np

cam = cv2.VideoCapture(0)

pts = []


def mouse(event, x, y, flags, param):
    counter = 0
    if event == cv2.EVENT_LBUTTONDOWN:
        if counter == 0:
            counter = counter + 1
            cv2.imwrite('template.jpg', display)

        pts.append((x, y))


while True:
    x, display = cam.read()
    cv2.namedWindow('display')
    cv2.setMouseCallback('display', mouse)
    img = cv2.imread('template.jpg')

    if len(pts) == 2:
        template_cropped = img[pts[0][1]:pts[1][1], pts[0][0]:pts[1][0]]
        cv2.imshow('cropped', template_cropped)
        template_gray = cv2.cvtColor(template_cropped, cv2.COLOR_BGR2GRAY)
        width = template_cropped.shape[1]
        height = template_cropped.shape[0]

        img_gray = cv2.cvtColor(display, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.8)

        for x, y in zip(*loc[::-1]):
            cv2.rectangle(display, (x, y), (x + height, y + width), (0, 255, 0), 1)
            cv2.putText(display, 'OBJECT', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

    cv2.imshow('display', display)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break