from tkinter import *
import tkinter as tk
from tkinter import filedialog, Text
from PIL import Image, ImageTk
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd='C:\Program Files\Tesseract-OCR'


def open_img():
    filename = filedialog.askopenfilename(initialdir='/Users/Desktop/', title='Select an Image',
                                          filetypes=(('JPG', '*.jpg'), ('All files', '*.*')))
    print(filename)
    global image, cropped
    image = cv2.imread(filename)
    cropped = image.copy()
    cv2.imshow('frame', image)
    cv2.waitKey(0)


def blur_img():
    global cropped, image
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((2, 2))
    gaussian_blur = cv2.GaussianBlur(image_gray, (5, 5), 2)
    cropped = gaussian_blur.copy()
    cv2.imshow('blur', gaussian_blur)


def auto_crop():
    global crop_auto, image

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_gray_smooth = cv2.GaussianBlur(image_gray, (5, 5), 0)
    ret, image_gray_smooth_thresh = cv2.threshold(image_gray_smooth, 180, 255, cv2.THRESH_BINARY)
    canny = cv2.Canny(image_gray_smooth_thresh, 150, 300)

    contour, heirarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    areas = [cv2.contourArea(c) for c in contour]
    max_index = np.argmax(areas)
    max_contour = contour[max_index]

    perimeter = cv2.arcLength(max_contour, True)
    coordinates = cv2.approxPolyDP(max_contour, 0.01 * perimeter, True)
    # cv2.drawContours(img, [coordinates], -1, (0,0,255), 5)

    pt1 = np.array([coordinates[1], coordinates[0], coordinates[2], coordinates[3]], np.float32)
    pt2 = np.array([(0, 0), (700, 0), (0, 600), (700, 600)], np.float32)

    pers = cv2.getPerspectiveTransform(pt1, pt2)
    crop_auto = cv2.warpPerspective(image, pers, (700, 600))
    # crop_auto = cv2.rotate(crop_auto, cv2.ROTATE_90_COUNTERCLOCKWISE)

    cv2.imshow('Auto Cropped', crop_auto)

    return (crop_auto)


def manual_crop():
    global crop_manual, image
    pts = []

    counter = 0

    def mouse(event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            if (x, y) is not None:
                pts.append((x, y))
                # print((x,y))

            if len(pts) == 4:
                print(pts)
                pt1 = np.array([pts[0], pts[1], pts[3], pts[2]], np.float32)
                pt2 = np.array([(0, 0), (700, 0), (0, 600), (700, 600)], np.float32)
                pers = cv2.getPerspectiveTransform(pt1, pt2)
                crop_manual = cv2.warpPerspective(image, pers, (700, 600))
                cv2.imshow('Manual Crop', crop_manual)
                return (crop_manual)

    cv2.namedWindow('frame')
    cv2.imshow('frame', image)
    cv2.setMouseCallback('frame', mouse)


def OCR_btn():
    global image, text, ocr_image
    ret, global_thresh = cv2.threshold(image, 170, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(global_thresh, lang='eng')
    data = pytesseract.image_to_data(global_thresh, output_type=Output.DICT)
    no_word = len(data['text'])

    for i in range(no_word):
        if int(data['conf'][i]) > 50:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            cv2.rectangle(global_thresh, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('OCR', global_thresh)
            cv2.waitKey(200)
    'cropped=global_thresh.copy()'
    ocr_image = global_thresh.copy()


def show_text():
    global text
    textbox = tk.Frame(frame, bg='#FDFFD6')
    textbox.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.6)
    textframe = Text(textbox, bg='#FDFFD6')
    textframe.insert('1.0', text)
    textframe.pack()


def save_img():
    global ocr_image
    filename = filedialog.asksaveasfilename(initialdir='/Users/Desktop/', title='Save File',
                                            filetypes=(('JPG', '*.jpg'), ('All files', '*.*')))
    print(filename)
    cv2.imwrite(filename, ocr_image)



def Close_All_Windows():
    cv2.destroyAllWindows()

root = tk.Tk()
root.title('OCR')
image = np.zeros((), np.uint8)
cropped = np.zeros((), np.uint8)
ocr_image = np.zeros((), np.uint8)
text = ""
canvas = tk.Canvas(root, height=720, width=1080, bg='green')
canvas.pack()
frame = tk.Frame(root, bg='black')
frame.place(relwidth=0.6, relheight=0.8, relx=0.2, rely=0.05)
textbox = tk.Frame(frame, bg='grey')
textbox.place(relwidth=0.6, relheight=0.6, relx=0.2, rely=0.2)


label = tk.Label(frame, text='TEXT', fg='black', bg='white', font=('Arial black', 20))
label.place(relx=0.2, rely=0.1)

open_img_btn = tk.Button(canvas, text='Open Image', fg='black', padx=5, pady=5, command=open_img)
open_img_btn.place(relx=0.04, rely=0.1)

blur_img_btn = tk.Button(canvas, text='Blur Image', fg='black', padx=5, pady=5, command=blur_img)
blur_img_btn.place(relx=0.038, rely=0.2)

auto_crop_btn = tk.Button(canvas, text='Auto Crop', fg='black', padx=5, pady=5, command=auto_crop)
auto_crop_btn.place(relx=0.038, rely=0.3)

manual_crop_btn = tk.Button(canvas, text='Manual Crop', fg='black', padx=5, pady=5, command=manual_crop)
manual_crop_btn.place(relx=0.035, rely=0.4)

OCR_btn = tk.Button(canvas, text='OCR', fg='black', padx=20, pady=5, command=OCR_btn)
OCR_btn.place(relx=0.85, rely=0.1)

show_text_btn = tk.Button(canvas, text='Show text', fg='black', padx=5, pady=5, command=show_text)
show_text_btn.place(relx=0.85, rely=0.2)

save_img_btn = tk.Button(canvas, text='Save Image', fg='black', padx=5, pady=5, command=save_img)
save_img_btn.place(relx=0.85, rely=0.3)

Close_All_Windows_btn = tk.Button(canvas, text='Close All Windows', padx=10, pady=10, command=Close_All_Windows)
Close_All_Windows_btn.place(relx=0.8, rely=0.9)

root.mainloop()
