import customtkinter as ctk
from tkinter import messagebox
from .ButtonsFunctionalities import ButtonsFunctionalities
import matplotlib.pyplot as plt
from .ImagesIO import ImagesIO


class HistogramControls(ButtonsFunctionalities):
    #HistogramControls crea las funcionalidades y botónes de lasección histograma del menu

    def __init__(self, menuPanel,  tabView, openedImages, createdTabs):
        #Constructor

        super().__init__(tabView, openedImages, createdTabs)
        self.menuPanel = menuPanel

        #Creamos los boones
        self.createControls()

    def createControls(self):
        #Esta función crea los botones

        #Botón para crear histograma
        ctk.CTkButton(self.menuPanel,text="Obtener el histograma",
                    fg_color="#FFA600",
                    command=lambda: self.getHistogram()).pack(fill="x", padx=15, pady=20)

    def getHistogram(self):
        #Esta función se ejecuta cuando el usuario presiona el botón "Obtener el histograma"

        image,name =self.getImage()

        if image is None:
            return

        # Mostrar histograma en ventana aparte
        figure = self.histogram.showHistogram(image, name)
        figure.canvas.mpl_connect('close_event',lambda event: self.saveHistogram(figure, name))
        plt.show()

    def saveHistogram(self, histogram, name):
        #Esta función pregunta si se quiere guardar el histograma antes de cerrar

        #Preguntamos
        answer=messagebox.askyesno("Guardar histograma","¿Quieres guardar el histograma?")

        if answer:
            image = ImagesIO.figToCV(histogram)
            #Guardamos en caso de que si quiera guardarla
            if image is not None:
                result = ImagesIO.saveFile(image, "Histograma de "+str(name))

                if result:
                    messagebox.showinfo("Éxito", "Imagen guardada con éxito")
                elif result is False:
                    messagebox.showerror("Error", "No se pudo guardar la imagen")
