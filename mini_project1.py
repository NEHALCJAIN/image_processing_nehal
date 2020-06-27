import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import pytesseract
from pytesseract import Output


count=0

imgage= np.array ([0],np.uint8)
crop = np.array ([0],np.uint8)
display = np.array ([0],np.uint8)
clicks = np.zeros((4, 2),np.float32)



def image_opening():
    global imgage

    img= filedialog.askopenfilename (initialdir = 'E:\giu', title = 'Select Image', filetypes = (('JPG', '*.jpg'), ('All files', '*.*')))
    imgage = cv2.imread (img)

    cv2.namedWindow ('OG', cv2.WINDOW_NORMAL)
    cv2.imshow ('OG', imgage)





def man_tran():
    cv2.setMouseCallback ('OG', clicking)




def clicking(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global count
        global clicks
        global imgage

        if (count< 4):
            clicks[count] = [x, y]
            count+= 1
            print ('you clicked pts')
            imgCopy = np.copy (imgage)
            cv2.imshow ('OG', imgCopy)

            if np.all (clicks):
                warping ()
        else:
            pass


def warping():
    global clicks
    global imgage
    global crop

    warpedPoints = np.array ([(0, 0), (720, 0), (0,1080), (720, 1080)], dtype = np.float32)

    perspective = cv2.getPerspectiveTransform (clicks, warpedPoints)
    warped = cv2.warpPerspective (imgage, perspective, (720, 1080))

    global display
    display = warped
    img_display()
    crop= warped



def img_display():
    global display

    cv2.namedWindow ('crop', cv2.WINDOW_NORMAL)
    cv2.imshow ('crop', display)


def saveImage ():
    global display
    cv2.imwrite('new1.jpg', display)


def showText ():
    global crop

    croppedGrey = cv2.cvtColor (crop, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold (croppedGrey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 35)
    data = pytesseract.image_to_data (thresh, output_type = Output.DICT)
    numberWord = len (data['text'])

    for i in range (numberWord):
        x, y, width, height = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        cv2.rectangle (crop, (x, y), (x+width, y+height), (255, 0, 0), 1)

    global display
    display = crop
    img_display()



def closeAllWindows():
    cv2.destroyAllWindows()



root =tk.Tk()
canvas = tk.Canvas (root, height = 720, width = 1080 ,bg = 'green')
canvas.pack()

frame = tk.Frame(canvas, bg='white')
frame.place(relx=0.1, rely=0.05, relwidth=0.6, relheight=0.9)

image_opening = tk.Button (canvas, text = 'Open Image', padx = 10, pady = 10, command = image_opening)
image_opening.place (relx = 0.9, rely = 0.1, anchor = 'n')

man_tran= tk.Button (canvas, text = 'Manual Crop', padx = 10, pady = 10, command = man_tran)
man_tran.place (relx = 0.9, rely = 0.3, anchor = 'n')

saveImage = tk.Button (canvas, text = 'Save Image', padx = 10, pady = 10, command = saveImage)
saveImage.place (relx = 0.9, rely = 0.5, anchor = 'n')


showText = tk.Button (canvas, text = 'Show Text', padx = 10, pady = 10, command = showText)
showText.place (relx = 0.9, rely = 0.7, anchor = 'n')

closeWindows = tk.Button (canvas, text = 'Close All Windows', padx = 10, pady = 10, command = closeAllWindows)
closeWindows.place (relx = 0.9, rely = 0.9, anchor = 'n')




root.mainloop()