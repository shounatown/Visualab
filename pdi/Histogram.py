import cv2
import numpy as np
import matplotlib.pyplot as plt
from .ColorMap import ColorMap

class Histogram:
    #Histogram se encarga de trabajar con las herramientas relacionadas a la generación del histograma

    def __init__(self):
        self.cm = ColorMap()

    def showHistogram(self, image, name):
        #Función que genera el histograma
        histogram=plt.figure()
        x=np.arange(256)
        #Si es a color
        if len(image.shape)==3:
            colors=('b','g','r')
            imageGray = self.cm.applyGrayScale(image)

            for i, color in enumerate(colors):
                hist = cv2.calcHist([image], [i], None, [256], [0, 256]).flatten()
                plt.bar(x, hist, color=color, alpha=0.4, width=1)

            hist = cv2.calcHist([imageGray], [0], None, [256], [0, 256]).flatten()
            plt.bar(x, hist, color='gray', alpha=0.4, width=1)


        else:
            hist = cv2.calcHist([image], [0], None, [256], [0, 256]).flatten()
            plt.bar(x, hist, color='gray', width=1)

        #nombrar el histograma
        plt.title("Histograma de " + str(name))
        plt.xlim([-5, 260])

        return histogram
