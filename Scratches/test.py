import cv2
import tkinter as tk
import matplotlib.pyplot as plt


# def show_values():
#     print(w1.get(), w2.get())
#
#
# master = Tk()
# w1 = Scale(master, from_=0, to=42)
# w1.set(19)
# w1.pack()
# w2 = Scale(master, from_=0, to=200, orient=HORIZONTAL)
# w2.set(23)
# w2.pack()
# Button(master, text='Show', command=show_values).pack()
#
# mainloop()

originalImage = cv2.imread('/Users/miles/Documents/Python Projects/coding etc/Ed Hammill/Practice Miles sequence/0.17sec-image000.jpg')
grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

(thresh, blackAndWhiteImage1) = cv2.threshold(grayImage, 127, 200, cv2.THRESH_BINARY)
(thresh, blackAndWhiteImage2) = cv2.threshold(grayImage, 200, 200, cv2.THRESH_BINARY) 

#cv2.imshow('Black white image1', blackAndWhiteImage1)
#cv2.imshow('Black white image2', blackAndWhiteImage2)





# cv2.imshow('Original image',originalImage)
# cv2.imshow('Gray image', grayImage)
  
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# Parameters
# You need to pass four parameters to cv2 threshold() method.

# src:Input Grayscale Image array.
# thresholdValue: Mention that value which is used to classify the pixel values.
# maxVal: The value to be given if pixel value is more than (sometimes less than) the threshold value.
# thresholdingTechnique: The type of thresholding to be applied.
    # There are 5 different simple thresholding techniques are :

    # cv2.THRESH_BINARY: If pixel intensity is greater than the set threshold, value set to 255, else set to 0 (black).
    # cv2.THRESH_BINARY_INV: Inverted or Opposite case of cv2.THRESH_BINARY.<li.
    # cv2.THRESH_TRUNC: If pixel intensity value is greater than threshold, it is truncated to the threshold. The pixel values are set to be the same as the threshold. All other values remain the same.
    # cv2.THRESH_TOZERO: Pixel intensity is set to 0, for all the pixels intensity, less than the threshold value.
    # cv2.THRESH_TOZERO_INV: Inverted or Opposite case of cv2.THRESH_TOZERO.
