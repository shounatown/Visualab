from tkinter import filedialog
import cv2
import numpy as np

class ImagesIO:
    #ImagesIO se encarga de la entrada y la salida de archivos

    def selectFile():
        #Esta función abre el explorador y retorna la ruta del archivo

        return filedialog.askopenfilename(
            #Extensiones permitidas
            filetypes=[("Imágenes", "*.jpg *.png *.bmp *.jpeg")]
        )

    def openImage(path):
        #Esta función carga la imagen con OpenCV y retorna el objeto Image

        try:
            #Abrir la imagen con OpenCV
            image = cv2.imread(path, cv2.IMREAD_COLOR)
            #Validar
            if image is None:
                print("Error: no se pudo leer la imagen")
                return None
            return image
        #Capturar excepcion
        except Exception as e:
            print("Error al abrir la imagen :( \n" + str(e))
            return None

    def saveFile(image, defaultName):
        #Esta función guarda la imagen en el dispositivo

        if image is None:   #revisa si hay imagen para guardar
            return False

        filePath = filedialog.asksaveasfilename(
            #Extensiones .png por default
            defaultextension=".png",
            initialfile=defaultName,
            filetypes=[("PNG", "*.png"), ("JPG", "*.jpg"), ("Todos", "*.*")]
        )

        if filePath:
            try:
                #Guardar con OpenCV
                cv2.imwrite(filePath, image)
                return True
            except Exception as e:
                print("Error al guardar la imagen :( \n" + str(e))
                return False
        return None

    def figToCV(fig):
        #Esta función convierte una figura de Matplotlib en un array de OpenCV
        try:
            #Dibujar el canvas
            fig.canvas.draw()

            #Convertir el canvas a un array de números
            image = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
            w, h = fig.canvas.get_width_height()
            image = image.reshape((h, w, 4))[:, :, :3]

            #Convertir de RGB a BGR
            finalImage = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            return finalImage
        except Exception as e:
            print("Error al convertir figura: "+str(e))
            return None