import cv2
from tkinter import messagebox


class ImageOperations:
    #Esta clase maneja las funciones para hacer operaciones entre imágenes

    def addition(self, imageA, imageB):
        #Función para sumar dos imágenes
        return cv2.add(imageA, imageB)

    def subtraction(self, imageA, imageB):
        #Función para restar dos imágenes
        return cv2.subtract(imageA, imageB)

    def multiplication(self, imageA, imageB):
        #Función para multiplicar dos imágenes
        return cv2.multiply(imageA, imageB)

    def division(self, imageA, imageB):
        #Función para dividir dos imágenes
        return cv2.divide(imageA, imageB)

    def AND(self, imageA, imageB):
        #Función para aplicar AND a dos imágenes
        return cv2.bitwise_and(imageA, imageB)

    def OR(self, imageA, imageB):
        #Función para aplicar Or a dos imágenes
        return cv2.bitwise_or(imageA, imageB)

    def XOR(self, imageA, imageB):
        #Función para aplicar XOR a dos imágenes
        return cv2.bitwise_xor(imageA, imageB)

    def isCompatible(self, imageA, imageB):
        #Función que compara alto, ancho y canales
        return imageA.shape == imageB.shape

    def matchChannels(self, imageA, imageB):
        #Función para igualar los canales de dos imágenes
        if len(imageA.shape)!= len(imageB.shape):
            #Preguntamos si quiere convertir
            if messagebox.askyesno("Los canales no coinciden", "¿Igualar ambos canales?"):
                #La de menos canales la convertimos a más
                if len(imageA.shape)<len(imageB.shape):
                    imageA=cv2.cvtColor(imageA, cv2.COLOR_GRAY2BGR)
                else:
                    imageB=cv2.cvtColor(imageB, cv2.COLOR_GRAY2BGR)
                return imageA, imageB
            else:
                #Informamos que no se pudo realizar
                messagebox.showwarning("Atención","No se pudo realizar la operación debido a que no son compatibles en número de canales")
                return None, None
        return imageA, imageB

    def matchSize(self, imageA, imageB):
        #Función para igualar el tamaño de las imágenes si son diferentes usamos imageA como tamaño base
        if imageA.shape[:2]!=imageB.shape[:2]:
            #Preguntamos si quiere escalar
            if messagebox.askyesno("El tamaño es distinto", "¿Redimensionar la segunda imagen?"):
                h, w=imageA.shape[:2]
                #escalamos
                imageB=cv2.resize(imageB, (w, h))
                return imageA, imageB
            else:
                #Informamos que no se pudo realizar
                messagebox.showwarning("Atención","No se pudo realizar la operación debido a que no son compatibles en tamaño")
                return None, None
        return imageA, imageB

