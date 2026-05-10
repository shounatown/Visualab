import cv2

class BasicOperations:
    #Esta clase maneja las funciones para hacer operaciones básicas

    def scalarAddition(self, image, scalar):
        #Función para sumar un escalar una imagen
        return cv2.add(image, scalar)

    def scalarSubtraction(self, image, scalar):
        #Función para restar un escalar una imagen
        return cv2.subtract(image, scalar)

    def scalarMultiplication(self, image, scalar):
        #Función para multiplicar un escalar una imagen
        return cv2.multiply(image, scalar)

    def scalarDivision(self, image, scalar):
        #Función para dividir un escalar una imagen
        return cv2.divide(image, scalar)

    def negative(self, image):
        #Función para sacar el negativo de una imagen
        return 255-image

    def umbralize(self, image, umbral):
        #Función para sacar el negativo de una imagen
        _, result = cv2.threshold(image, umbral, 255, cv2.THRESH_BINARY)
        return result

