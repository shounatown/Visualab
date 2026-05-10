import cv2
import numpy as np

class Connectivity:
    #Esta clase maneja las funciones para hacer la conectividad

    def preprocessImage(self, image):
        #Función para preparar la imagen para la conectividad
        #Si es a color la hacemos primero a grises
        if len(image.shape)==3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #Contamos los valores unicos con unique para saber si es binari
        if len(np.unique(image))>2:
            #Usamos OTSU para que se agarre el "mejor" umbral
            _, binary=cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        else:
            binary=image
        return binary

    def useColorMap(self, image, connectivity=4):
        #Función para contar con los colores
        binary=self.preprocessImage(image)

        #Aplicar etiquetado
        #labels es una matriz del mismo tamaño que la imagen pero con los números de los objetos que son
        numLabels, labels=cv2.connectedComponents(binary, connectivity=connectivity)

        #Creamos un mapa de colores usando HUE de 0-179
        coloresHUE=np.uint8(179*labels/np.max(labels))
        blank=np.ones_like(coloresHUE)*255 #Matriz de puro blanco

        #Imagen a HSV y luego convertimos a BGR
        hsvImage = cv2.merge([coloresHUE, blank, blank])
        colorImage = cv2.cvtColor(hsvImage, cv2.COLOR_HSV2BGR)

        #El fondo tiene que ser negro
        colorImage[labels==0]=0

        #Restamos 1 al conteo porque el fondo no es un objeto).
        return colorImage, numLabels-1

    def useLabels(self, image, connectivity):
        #Funciòn para mostrar la conectividad con etiquetas
        binary=self.preprocessImage(image)

        if connectivity==4:
            #Obtenemos estadísticas y centroides
            numLabels, labels, medidas, center= cv2.connectedComponentsWithStats(binary, connectivity=4)

            #Convertir a color para dibujar
            colorImage=cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

            #Empezamos desde 1 para ignorar el fondo
            for i in range(1, numLabels):
                x, y, w, h=medidas[i, cv2.CC_STAT_LEFT],medidas[i, cv2.CC_STAT_TOP],medidas[i, cv2.CC_STAT_WIDTH], medidas[i, cv2.CC_STAT_HEIGHT]
                cx, cy = center[i]

                # Dibujar rectángulo verde
                cv2.rectangle(colorImage, (x, y), (x+w,y+h), (0, 255, 0), 2)

                #Dibujar número
                cv2.putText(colorImage, str(i), (int(cx)-5, int(cy)+5),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            #numLabels-1 porque el fondo no es un objeto
            return colorImage, numLabels-1

        else:
            #Buscar contornos
            contours, _=cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Convertimos la imagen a color para poder dibujar los contornos y los numeros
            colorImage= cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

            #Dibujar los contornos y numerar los objetos
            for i, contour in enumerate(contours):
                #dibujamos en verde y 2 de grosor
                cv2.drawContours(colorImage, [contour], -1, (0, 255, 0), 2)

                #Obtener el centro paraponer el numero
                x, y, w, h = cv2.boundingRect(contour)
                cv2.putText(colorImage, str(i+1), (x, y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            return colorImage, len(contours)

