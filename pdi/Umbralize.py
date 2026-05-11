import customtkinter as ctk
import cv2
import numpy as np

class Umbralize:

    def openHSVWindow(self, image, name, showResultFunction):
        #Función para la ventana de umbralizado
        self.image = image
        self.name = name
        self.showResultFunction = showResultFunction

        self.hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        self.window = ctk.CTkToplevel()
        self.window.title("Umbral HSV")
        self.window.geometry("400x500")

        #Valores minimos
        ctk.CTkLabel(self.window, text="Mínimos").pack(pady=10)

        self.sliderHMin = self.createSliderWindow("H Min", 0, 179, 0)
        self.sliderSMin = self.createSliderWindow("S Min", 0, 255, 0)
        self.sliderVMin = self.createSliderWindow("V Min", 0, 255, 0)

        #Valores máximos
        ctk.CTkLabel(self.window, text="Máximos").pack(pady=10)

        self.sliderHMax = self.createSliderWindow("H Max", 0, 179, 179)
        self.sliderSMax = self.createSliderWindow("S Max", 0, 255, 255)
        self.sliderVMax = self.createSliderWindow("V Max", 0, 255, 255)

        # Boton
        ctk.CTkButton(self.window,text="Aplicar",command=self.umbralizeHSV).pack(pady=20)

        self.updatePreviewHSV()

    def createSliderWindow(self, text, from_, to, default):
        #Crear sliders para umbralizado

        #Crear etiqueta de los sliders
        label = ctk.CTkLabel(self.window, text=str(text)+": "+ str(default))
        label.pack()

        #Crear slider
        slider = ctk.CTkSlider(self.window,from_=from_,to=to,number_of_steps=to-from_,
                            command=lambda v: self.updateSliderWindow(label, text, v))

        slider.set(default)
        slider.pack(fill="x", padx=20, pady=5)

        return slider

    def updateSliderWindow(self, label, text, value):
        #Actualizar slider
        label.configure(text=str(text)+": "+ str(int(value)))
        self.updatePreviewHSV()

    def getLowerUpper(self):
        #Función para obtener los valores máximos y mínimos de los slider
        lower = np.array([
            int(self.sliderHMin.get()),
            int(self.sliderSMin.get()),
            int(self.sliderVMin.get())
        ])
        upper = np.array([
            int(self.sliderHMax.get()),
            int(self.sliderSMax.get()),
            int(self.sliderVMax.get())
        ])

        return lower, upper

    def updatePreviewHSV(self):
        #Actualizar vista del umbralizado por canales HSV
        lower, upper = self.getLowerUpper()
        mask = cv2.inRange(self.hsv, lower, upper)
        cv2.imshow("Vista previa HSV", mask)

    def umbralizeHSV(self):
        #Aplicar el umbralizado por canales HSV
        lower, upper = self.getLowerUpper()
        mask= cv2.inRange(self.hsv, lower, upper)
        self.showResultFunction(mask,self.name,"umbralHSV")
        cv2.destroyWindow("Vista previa HSV")
        self.window.destroy()