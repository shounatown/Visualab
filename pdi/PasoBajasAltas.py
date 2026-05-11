import cv2
import numpy as np


class PasoBajasAltas:
    #Filtro máximo
    def filtroMaximo(self, img, size=3):
        fil, col=img.shape
        pad=size//2
        wMax= np.zeros((fil+pad*2, col+pad*2), np.uint8)
        imageMax=np.zeros((fil, col), np.uint8)

        for j in range(pad, fil+pad):
            for i in range(pad, col+pad):
                wMax[j, i]=img[j-pad, i-pad]
                ventana=wMax[j-pad : j+pad+1, i-pad : i+pad+1]
                imageMax[j-pad, i-pad] = np.amax(ventana)

        return imageMax

    #Filtro mínimo
    def filtroMinimo(self, img, size=3):
        fil, col = img.shape
        pad = size//2
        wMin = np.ones((fil+pad*2, col+pad*2), np.uint8)*255
        imageMin = np.zeros((fil, col), np.uint8)

        for j in range(pad, fil+pad):
            for i in range(pad, col+pad):
                wMin[j, i] = img[j-pad, i-pad]
                ventana = wMin[j-pad : j+pad+1, i-pad : i+pad+1]
                imageMin[j-pad, i-pad] = np.amin(ventana)

        return imageMin
    
    def medianBlur(self, image, kernel):
        return cv2.medianBlur(image, kernel)