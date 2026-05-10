import cv2
import numpy as np

class GeometricTransformations:
    #Esta clase maneja las funciones para hacer transformaciones geométricas

    def translate(self, image, tx, ty):
        #Función para trasladar una imagen
        h, w= image.shape[:2]       #Obtener alto y ancho
        matrizTrans = np.float32([[1, 0, tx],[0, 1, ty]])
        return cv2.warpAffine(image, matrizTrans, (w, h))

    def rotate(self, image, angle):
        #Funció para rotar alrededor del centro
        h, w = image.shape[:2]      #Obtener alto y ancho
        matrizRot = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
        return cv2.warpAffine(image, matrizRot, (w, h))

    def scale(self, image, fx, fy):
        #Función para escalado en X y Y
        return cv2.resize(image, None, fx=fx, fy=fy)

    def scalePX(self, image, fx, fy):
        #Función para escalado en X y Y con px
        return cv2.resize(image, (fx,fy))

    def reflect(self, image, mode):
        #Función para reflejar imagen
        #0 horizontal, 1 vertical
        if mode=="horizontal":
            return cv2.flip(image, 1)
        elif mode == "vertical":
            return cv2.flip(image, 0)
        return image

