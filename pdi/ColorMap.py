import cv2
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import json
import os
import sys


class ColorMap:
    #Esta clase maneja las funciones para aplicar color maps
    def __init__(self):
        #Constructor
        #Mapas de color definidos en OpenCV
        self.maps = {
            "Autumn": cv2.COLORMAP_AUTUMN,
            "Bone": cv2.COLORMAP_BONE,
            "Cividis":cv2.COLORMAP_CIVIDIS,
            "Cool": cv2.COLORMAP_COOL,
            "Deep green": cv2.COLORMAP_DEEPGREEN,
            "Hot": cv2.COLORMAP_HOT,
            "HSV" : cv2.COLORMAP_HSV,
            "Inferno" : cv2.COLORMAP_INFERNO,
            "Jet": cv2.COLORMAP_JET,
            "Magma":  cv2.COLORMAP_MAGMA,
            "Ocean": cv2.COLORMAP_OCEAN,
            "Parula": cv2.COLORMAP_PARULA,
            "Pink": cv2.COLORMAP_PINK,
            "Plasma": cv2.COLORMAP_PLASMA,
            "Rainbow": cv2.COLORMAP_RAINBOW,
            "Spring" : cv2.COLORMAP_SPRING,
            "Summer" : cv2.COLORMAP_SUMMER,
            "Turbo": cv2.COLORMAP_TURBO,
            "Twilight" : cv2.COLORMAP_TWILIGHT,
            "Twilight shifted" : cv2.COLORMAP_TWILIGHT_SHIFTED,
            "Viridis" : cv2.COLORMAP_VIRIDIS,
            "Winter" : cv2.COLORMAP_WINTER
        }
        self.fileColorMap="data/colormaps.txt"
        #Nuevos mapas personalizados
        self.newMaps = {}
        #Cargar mapas
        self.loadNewMaps()

    def applyGrayScale(self, image):
        #Función para aplicar la escala de grises a una imaen
        if len(image.shape)==2: #Si ya es gris la retornamos
            return image
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def applyColorMap(self, image, colorMapName):
        #Si es una mapa personalizado
        if colorMapName in self.newMaps:
            colorMap=self.newMaps[colorMapName]
            #Normalizar la imagen ya que los colores están normalizados
            normalizada=image/255.0
            #Aplicar colormap
            imageColorMap=colorMap(normalizada)

            #Convertir a BGR OpenCV
            imageColorMap=(imageColorMap[:, :, :3]*255).astype(np.uint8)
            return cv2.cvtColor(imageColorMap, cv2.COLOR_BGR2RGB)
        else:
            #Si es de los predeterminados
            selected=self.maps.get(colorMapName, cv2.COLORMAP_JET)
            return cv2.applyColorMap(image, selected)

    def saveNewColorMap(self, name, colors):
        #Funciòn para guardar los nuevos color map

        #Leemos los color maps guardados
        with open(self.resourcePath(self.fileColorMap), "a") as f:
            f.write(json.dumps({"name": name, "colors": colors}) + "\n")

        #Crear colormap con LinearSegmentedColormap
        colorMap=LinearSegmentedColormap.from_list(name, colors, N=256)
        self.newMaps[name]=colorMap

    def loadNewMaps(self):
        #Función para cargar los nuevos color maps
        try:
            #Leemos el archivo
            with open(self.resourcePath(self.fileColorMap), "r") as f:
                for line in f:
                    data=json.loads(line)
                    colorMap=LinearSegmentedColormap.from_list(data["name"], data["colors"], N=256)
                    self.newMaps[data["name"]] = colorMap
        except FileNotFoundError:
            print("ERORR AL CARGAR LOS MAPITAS")

    def colorMapPreview(self, colorMapName):
        #Función para mostrar la vista previa del color map
        #Hacemos un gradiente para la vista previa
        gradient=np.linspace(0, 255, 256, dtype=np.uint8)
        gradient=np.tile(gradient, (50, 1))
        #Aplicamos el mapa de color al gradiente
        return self.applyColorMap(gradient, colorMapName)
    
    def resourcePath(self, relativePath):
        #Función para cargar recursos
        try:
            basePath = sys._MEIPASS
        except Exception:
            basePath = os.path.abspath(".")
        return os.path.join(basePath, relativePath)


