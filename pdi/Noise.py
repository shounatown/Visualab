import cv2
import numpy as np

class Noise:
    #Esta clase maneja las funciones para el ruido

    def gaussiano(self,image, media, sigma):
        #Función para aplicar el ruido gaussiano
        #Generamos una matriz de ruido con lacampana de gauss
        gauss=np.random.normal(media, sigma, image.shape).astype(np.int16)
        #Sumamos a la imagen original
        imageNoise=image.astype(np.int16)+gauss
        #arreglamos para que los valores sea de 0 a 255
        imageNoise=np.clip(imageNoise, 0, 255).astype(np.uint8)
        return imageNoise

    def saltAndPepper(self,image, cantidad, sal):
        #Función para aplicar el ruido sal y pimienta
        #Obtenemos las dimensiones de la imagen
        h,w=image.shape[:2]
        #Calculamos a cuántos píxeles le podremos ruido
        numNoise=int(cantidad*h*w)
        for _ in range(numNoise):
            #Elegimos coordenadas al azar
            i=np.random.randint(0,w)
            j=np.random.randint(0,h)
            if np.random.rand()<sal:
                image[j, i]=255#Sal
            else:
                image[j, i]=0#Pimienta
        return image

    def speckle(self, image, media, sigma):
        #Función que aplica el ruido speckle
        #Convertimos a float
        floatImage=image.astype(np.float32)

        #Generamos la matriz de ruido
        noise = np.random.normal(media, sigma, image.shape)
        #Aplicamos la formula
        imageNoise =floatImage+(floatImage*noise)
        #Arreglamos los valores de 0 a 255
        return np.clip(imageNoise, 0, 255).astype(np.uint8)

    def gaussianBlur(self, image, kernel, sigma):
        #Función que aplica el filtro gaussiano
        return cv2.GaussianBlur(image, (kernel,kernel), sigma)