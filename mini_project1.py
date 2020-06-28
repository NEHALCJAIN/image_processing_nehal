from tkinter import *
import tkinter as tk
from tkinter import filedialog, Text
from PIL import Image, ImageTk
import cv2
import numpy as np
import pytesseract as pt
from pytesseract import Output




def open():
    global img, cropped
    filename = filedialog.askopenfilename(initialdir='E://', title='Select an Image',
                                          filetypes=(('JPG', '*.jpg'), ('All files', '*.*')))
    print(filename)
    image = cv2.imread(filename)
    cropped = image.copy()
    cv2.imshow('frame', image)
    cv2.waitKey(0)


def blur():
    global cropped, image
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((2, 2))
    gaussian_blur = cv2.GaussianBlur(image_gray, (5, 5), 2)
    cropped = gaussian_blur.copy()
    cv2.imshow('frame', gaussian_blur)


def auto_crop():
    global cropped, image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5, 5))
    gaussian_blur = cv2.GaussianBlur(image, (5, 5), 2)

    edge = cv2.Canny(gaussian_blur, 40, 280)
    contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    max_contour = contours[max_index]
    perimeter = cv2.arcLength(max_contour, True)
    ROI = cv2.approxPolyDP(max_contour, 0.01 * perimeter, True)

    cv2.drawContours(img, [ROI], -1, (0, 255, 0), 2)

    pts_1 = np.array([ROI[0], ROI[1], ROI[3], ROI[2]], np.float32)
    pts_2 = np.array([(0, 0), (500, 0), (0, 500), (500, 500)], np.float32)

    perspective = cv2.getPerspectiveTransform(pts_1, pts_2)
    transformed = cv2.warpPerspective(perspective, (500, 500))

    cv2.imshow('output', transformed)


def manual_crop():
    pts = []

    def mouse(event, x, y, flags, param):
        global cropped, image
        if event == cv2.EVENT_LBUTTONDOWN:
            pts.append((x, y))
        if len(pts) == 4:
            warp(pts)

    def warp(pts):
        global cropped, image
        pts_1 = np.array([pts[0], pts[1], pts[3], pts[2]], np.float32)
        pts_2 = np.array([(0, 0), (720, 0), (0, 720), (720, 720)], np.float32)

        perspective = cv2.getPerspectiveTransform(pts_1, pts_2)
        transformed = cv2.warpPerspective(img, perspective, (720, 720))

        cropped = transformed.copy()
        cv2.imshow('frame', transformed)

    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', mouse)


def OCR_btn():
    global cropped, text
    ret, global_thresh = cv2.threshold(cropped, 170, 255, cv2.THRESH_BINARY)
    text = pt.image_to_string(global_thresh, lang='eng')
    data = pt.image_to_data(global_thresh, output_type=Output.DICT)
    no_word = len(data['text'])

    for i in range(no_word):
        if int(data['conf'][i]) > 50:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            cv2.rectangle(global_thresh, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('frame', global_thresh)
            cv2.waitKey(200)
    'cropped=global_thresh.copy()'


def show_text():
    global text
    textbox = tk.Frame(frame, bg='green')
    textbox.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.6)
    textframe = Text(textbox, bg='white')
    textframe.insert('1.0', text)
    textframe.pack()


def save():
    global cropped
    filename = filedialog.asksaveasfilename(initialdir='E:\giu', title='Save File',
                                            filetypes=(('JPG', '*.jpg'), ('All files', '*.*')))
    print(filename)
    cv2.imwrite(filename, cropped)




def Close_All_Windows():
    cv2.destroyAllWindows()

root = tk.Tk()
root.title('OCR')
image = np.zeros((), np.uint8)
cropped = np.zeros((), np.uint8)
canvas = tk.Canvas(root, height=720, width=1080, bg='green')
canvas.pack()
frame = tk.Frame(root, bg='black')
frame.place(relwidth=0.6, relheight=0.8, relx=0.3, rely=0.05)
textbox = tk.Frame(frame, bg='gray')
textbox.place(relwidth=0.6, relheight=0.6, relx=0.2, rely=0.2)


label = tk.Label(frame, text='TEXT ', fg='black', bg='white', font=('Arial', 20))
label.place(relx=0.4, rely=0.1)

open_img = tk.Button(canvas, text='Open Image', fg='black', padx=5, pady=5, command=open)
open_img.place(relx=0.04, rely=0.1)

blur_img = tk.Button(canvas, text='Blur Image', fg='black', padx=5, pady=5, command=blur)
blur_img.place(relx=0.04, rely=0.2)

auto_crop = tk.Button(canvas, text='Auto Crop', fg='black', padx=5, pady=5, command=auto_crop)
auto_crop.place(relx=0.04, rely=0.3)

manual_crop = tk.Button(canvas, text='Manual Crop', fg='black', padx=5, pady=5, command=manual_crop)
manual_crop.place(relx=0.04, rely=0.4)

OCR_ = tk.Button(canvas, text='OCR', fg='black', padx=20, pady=5, command=OCR_btn)
OCR_.place(relx=0.4, rely=0.1)

show_text = tk.Button(canvas, text='Show text', fg='black', padx=5, pady=5, command=show_text)
show_text.place(relx=0.04, rely=0.5)

save_img = tk.Button(canvas, text='Save Img', fg='black', padx=5, pady=5, command=save)
save_img.place(relx=0.04, rely=0.6)

Close_All_Windows_btn = tk.Button(canvas, text='Close Windows', padx=10, pady=10, command=Close_All_Windows)
Close_All_Windows_btn.place(relx=0.04, rely=0.7)

root.mainloop()
