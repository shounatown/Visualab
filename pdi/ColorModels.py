import cv2
import numpy as np
from tkinter import messagebox

class ColorModels:
    #Esta clase maneja las funciones para hacer conversión entre modelos de color

    def  rgbTohsv(self, image):
        if len(image.shape)<3:
            messagebox.showerror("Error","La imagen debe tener 3 canales (RGB/BGR)")
            return None
        else:
            hsv=cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            h,s,v=cv2.split(hsv)
            return h,s,v

    def joinHSV(self, h,s,v):
        hsv= cv2.merge([h,s,v])
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return bgr
