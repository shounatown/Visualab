import cv2
import numpy as np
from tkinter import messagebox

class Ecualization:
    #Esta clase maneja las funciones para la ecualizacion

    def normalEcualization(self, image):
        if len(image.shape)>2:
            image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            messagebox.showinfo("Atención","La imagen fue convertida a escala de grises")
        return cv2.equalizeHist(image)