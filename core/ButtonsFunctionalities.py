from .ImagesIO import ImagesIO
import sys
import os
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from pdi.ColorMap import ColorMap
from pdi.Histogram import Histogram
from pdi.GeometricTransformations import GeometricTransformations
from pdi.BasicOperations import BasicOperations
from pdi.ImageOperations import ImageOperations
from pdi.Connectivity import Connectivity
from pdi.Noise import Noise
from pdi.ColorModels import ColorModels
from pdi.Ecualization import Ecualization
from pdi.Umbralize import Umbralize
from pdi.PasoBajasAltas import PasoBajasAltas
from pdi.MathematicalMorphology import MathematicalMorphology
from pdi.Segmentation import Segmentation
from PIL import Image
import cv2
import numpy as np

class ButtonsFunctionalities:
    #ButtonsFunctionalities es la clase encargada de darle funcionalidad a todos los botones de la interfaz

    def __init__(self, tabView, openedImages, createdTabs):
        #Constructor de la clase

        self.tabView = tabView              #Pestañas abiertas
        self.openedImages = openedImages    #Diccionario de las imágenes PIL
        self.createdTabs = createdTabs      #Set con las imágenes creadas
        self.combos = {}                    #Combo box de imagenes

        self.cm = ColorMap()
        self.histogram = Histogram()
        self.gt = GeometricTransformations()
        self.bo = BasicOperations()
        self.io = ImageOperations()
        self.conn = Connectivity()
        self.noise = Noise()
        self.colorModels = ColorModels()
        self.ec = Ecualization()
        self.u = Umbralize()
        self.pba = PasoBajasAltas()
        self.mm = MathematicalMorphology()
        self.seg = Segmentation()


    ##################Botones para el manejo de archivos##################

    def openImage(self):
        #Esta función se ejecuta cuando el usuario presiona el botón "Cargar imagen"

        #Abrir explorador de archivos
        path = ImagesIO.selectFile()

        #Verificar que el usuario sí seleccionó un archivo
        if path:
            #Obtener el nombre del archivo
            name = os.path.basename(path)

            #Evitar duplicados
            if name in self.createdTabs:
                messagebox.showerror("Error", "Ya hay una imagen abierta con el mismo nombre")
                return

            #Cargar imagen con OpenCV
            imageCV = ImagesIO.openImage(path)

            # Validar
            if imageCV is None:
                messagebox.showerror("Error", "No se pudo abrir la imagen")
                return

            #Crear nueva pestaña para mostrar la imagen
            self.tabView.add(name)
            self.createScroll(name, imageCV)

            #Registrar que se creó
            self.openedImages[name] = imageCV
            self.createdTabs.add(name)
            self.tabView.set(name)
            self.updateComboBoxImages()



    def saveImage(self):
        #Esta función se ejecuta cuando el usuario presiona el botón "Guardar imagen"

        image,name =self.getImage()

        if image is None:
            messagebox.showerror("Error", "No hay imagen cargada en esta pestaña")
            return

        #Guardar la imagen
        result = ImagesIO.saveFile(image, name)

        #Informar lo que ocurrió
        if result:
            messagebox.showinfo("Éxito", "Imagen guardada con éxito")
        elif result is False:
            messagebox.showerror("Error", "No se pudo guardar la imagen")

    def closeImage(self):
        #Esta función se ejecuta cuando el usuario presiona el botón "Cerrar pestaña actual"

        currentTab = self.tabView.get()

        #Validar que no es la pestaña de inicio
        if not self.validateTab(currentTab):
            return

        #Pedir la confirmación de cierre
        if messagebox.askyesno("Confirmar", "¿Estás seguro que quieres cerrar '"+str(currentTab)+"'?"):
            self.tabView.delete(currentTab)

            #Cerrar la pestaña
            self.openedImages.pop(currentTab, None)
            self.createdTabs.discard(currentTab)
            self.updateComboBoxImages()

            self.tabView.set("Inicio")


    ##################Funciones para la vista de imágenes##################

    def createScroll(self, name, imageCV):
        #Está función se encarga de crear un scroll para las imágenes grandes

        tab = self.tabView.tab(name)

        #Crear un canvas para poder scroller
        canvas = tk.Canvas(tab, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        #Scroll horizontal
        scrollY = tk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollY.pack(side="right", fill="y")

        #Scroll vertical
        scrollX = tk.Scrollbar(tab, orient="horizontal", command=canvas.xview)
        scrollX.pack(side="bottom", fill="x")

        canvas.configure(yscrollcommand=scrollY.set,xscrollcommand=scrollX.set)

        #panel donde va la imagen
        panelImage = ctk.CTkFrame(canvas, fg_color="transparent")

        window = canvas.create_window((0, 0),window=panelImage,anchor="nw")

        # Convertir imagen a CTK para que se pueda mostrar
        imageCTK = self.cv2ToCTK(imageCV)

        lbl = ctk.CTkLabel(panelImage, image=imageCTK, text="")
        lbl.image = imageCTK
        lbl.pack()

        #Evento: para cuando cambia el tamaño del canvas
        canvas.bind("<Configure>",lambda event: self.updateCanvas(canvas, panelImage, window))

        #Evento por si cambia el panel donde está la imagen
        panelImage.bind("<Configure>",lambda event: self.updateCanvas(canvas, panelImage, window))

        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda event: self.mouseWheel(canvas, event)))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))


    def updateCanvas(self, canvas, panelImag, window):
        #Función del evento para actualizar el canvar de la imagen

        #Actualizar scroll
        canvas.configure(scrollregion=canvas.bbox("all"))

        canvasWidth=canvas.winfo_width()
        canvasHeight= canvas.winfo_height()

        panelWidth = panelImag.winfo_reqwidth()
        panelHeight=panelImag.winfo_reqheight()

        #Centramos en X si es chiquito en x
        if panelWidth<canvasWidth:
            x = (canvasWidth-panelWidth)//2
        else:
            x=0

        #Centramos en y si es chiquito en y
        if panelHeight < canvasHeight:
            y = (canvasHeight-panelHeight)//2
        else:
            y= 0

        canvas.coords(window, x, y)


    def showResult(self, result, originalName, description):
        #Función par mostrar el resultado

        #Nombrar la imagen nueva
        name, type=os.path.splitext(originalName)
        newName = str(name)+"_"+str(description)+str(type)

        #Agregar número si se repite el nombre
        count=1
        while newName in self.createdTabs:
            newName=str(name)+"_"+str(description)+"("+str(count)+")"+str(type)
            count+=1

        #Añadir nombre nuevo
        self.tabView.add(newName)

        #Creamos el panel con scroll si es necesario
        self.createScroll(newName, result)

        #Registramos la reación de la imagen
        self.openedImages[newName] = result
        self.createdTabs.add(newName)
        self.tabView.set(newName)
        self.updateComboBoxImages()

    ##################Funciones extra##################

    def cv2ToCTK(self, imageCV):
        #Está función convierte una imagen de OpenCV a ctkImage para usarla en la interfaz

        #Convertir de openCV a PIL
        imageRGB = cv2.cvtColor(imageCV, cv2.COLOR_BGR2RGB)
        imagePIL = Image.fromarray(imageRGB)

        return ctk.CTkImage(light_image=imagePIL, dark_image=imagePIL, size=imagePIL.size)

    def validateTab(self, tab):
        #Función para validar que la pestaña no sea el inicio
        if tab=="Inicio":
            messagebox.showwarning("Aviso", "Selecciona una pestaña con imagen")
            return False
        return True

    def getImage(self):
        #Función para obtener la imagen actual
        currentTab=self.tabView.get()
        if not self.validateTab(currentTab):
            return None, None
        return self.openedImages[currentTab].copy(), currentTab

    def loadIcon(self, path, w, h):
        #Función para cargar icono
        image = Image.open(self.resourcePath(path))
        image = image.resize((w,h))
        return ctk.CTkImage(light_image=image, dark_image=image, size=(w,h))


##################Contenedores y botones######################

#ICONO Y LABEL
    def createIconButton(self, text, icon, command,color, colorHover, frame):
        #Función que crea botones con etiqueta a lado
        #Hacemos una fila para el boton
        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=5)

        #Cargamos la imagen
        icon = self.loadIcon(icon, 40, 40)

        #Creamos el boton
        button = ctk.CTkButton(row, image=icon,text="",
                            width=40,height=40,
                            corner_radius=8,border_width=0,
                            fg_color=color,hover_color=colorHover,
                            command=command)
        button.pack(side="left")
        button.image = icon

        #Creamos la etiqueta de a lado
        label = ctk.CTkLabel(row, text=text, font=("Arial", 12))
        label.pack(side="left", padx=10)

        return button

#PANEL CON SLIDER
    def createSliderPanel(self, name, icon, prefix, minValue, maxValue, command, last=""):
        #Esta función crea un panel con slider
        panel = ctk.CTkFrame(self.scrollFrame, corner_radius=15, border_width=1)
        panel.pack(fill="x", padx=10, pady=8)

        #Encabezado con icono
        icon=self.loadIcon(icon, 40,40)
        label=ctk.CTkLabel(panel, image=icon, text=str(name),compound="left", font=("Roboto", 14, "bold"))
        label.pack(side="top", anchor="nw", padx=15, pady=10)
        label.image=icon

        #Valor
        valueLabel= ctk.CTkLabel(panel, text=str(prefix)+": "+str(int((maxValue+minValue)/2)))
        valueLabel.pack()

        #Crear slider
        slider = ctk.CTkSlider(panel, from_=minValue, to=maxValue, command=lambda v: self.updateSlider(v, valueLabel, prefix, last))
        slider.pack(fill="x", padx=20, pady=5)

        # Botón de Aplicar
        ctk.CTkButton(panel, text="Aplicar "+str(name.lower()), fg_color="#FFA600",hover_color="#CC8500", command=command).pack(pady=10, padx=20, fill="x")

        return slider

    def updateSlider(self, value, slider, prefix="Valor", last=""):
        #Actualiza cualquier etiqueta de slider de forma genérica
        slider.configure(text=str(prefix)+": "+str(int(value))+str(last))

#PANEL NUMEROS FLECHA

    def createNumberPanel(self, name, icon, inputs, command, allowNegative=True):
        #Función para crear un panel para la entrado de números
        #Crear panel
        panel=ctk.CTkFrame(self.scrollFrame, fg_color="transparent", corner_radius=8, border_width=0)
        panel.pack(fill="x", padx=10, pady=10)

        #Cargar el icono y etiqueta
        icon=self.loadIcon(icon, 40, 40)
        label = ctk.CTkLabel(panel, image=icon, text=str(name),compound="left", font=("Roboto", 14, "bold"))
        label.pack(side="top", anchor="nw", padx=10, pady=5)
        label.image = icon

        #Crear  las cajas de números y guardarlas en una lista
        boxes = []
        for text in inputs:
            box=self.createNumberBox(panel, text, allowNegative=allowNegative)
            boxes.append(box)

        # Botón de Aplicar
        ctk.CTkButton(panel, text="Aplicar "+str(name.lower()), fg_color="#FFA600",hover_color="#CC8500", command=command).pack(pady=10, padx=20, fill="x")
        return boxes

    def createNumberBox(self, place, text, allowNegative=False):
        #Esta función crea una caja para poner números como entrada
        panel=ctk.CTkFrame(place)
        panel.pack(fill="x", pady=5)

        ctk.CTkLabel(panel, text=text).pack(side="left")
        variable = ctk.StringVar(value="1")

        entry = ctk.CTkEntry(panel, textvariable=variable, width=60)
        entry.pack(side="right", padx=5)

        #Botones arriba y abajo
        ctk.CTkButton(panel, text="▼", width=30, command= lambda: self.decrease(variable, allowNegative)).pack(side="right")
        ctk.CTkButton(panel, text="▲", width=30, command= lambda: self.increase(variable)).pack(side="right")

        return variable

    def increase(self, variable):
        #Función ligada a la caja numberBox
        try:
            #Obtener el número de la caja
            value = float(variable.get())
            value+=0.1
            #Actualizamos la variable en la interfaz
            variable.set(str(round(value, 2)))
        except:
            #Si esta mal reseteamos a 1
            variable.set("1")

    def decrease(self, variable, allowNegative):
        #Función ligada a la caja numberBox
        try:
            #Obtener el número de la caja
            value= float(variable.get())
            value-= 0.1
            if not allowNegative and value<= 0:
                return
            #Actualizamos la variable en la interfaz
            variable.set(str(round(value, 2)))
        except:
            #Si esta mal reseteamos a 1
            variable.set("1")

#PANEL RADIO BUTTON
    def createRadioButtonPanel(self, name, icon, inputs, command, default):
        #Función que crea un panel con RadioButton
        #Crear panel
        panel=ctk.CTkFrame(self.scrollFrame, fg_color="transparent", corner_radius=8, border_width=0)
        panel.pack(fill="x", padx=10, pady=10)

        #Icono y título
        icon=self.loadIcon(icon, 40, 40)
        label=ctk.CTkLabel(panel, image=icon, text=str(name), compound="left", font=("Roboto", 14, "bold"))
        label.pack(side="top", anchor="nw", padx=10, pady=5)
        label.image=icon

        #RadioButtons
        option = ctk.StringVar(value=default)

        #Generar RadioButtons
        for text, value in inputs:
            ctk.CTkRadioButton(panel, text=text, variable=option,value=value, hover_color="#FFA600",
                            fg_color="#FFA600").pack(anchor="w", padx=20, pady=2)

        #Botón de Aplicar
        ctk.CTkButton(panel, text="Aplicar "+str(name.lower()), fg_color="#FFA600",hover_color="#CC8500", command=command).pack(pady=10, padx=20, fill="x")
        return option
    

#PARA HACER UN COMBO BOX DE LAS IMAGENES CARGADAS
    def createComboBoxImages(self, key, place, text, values):
        #Esta función crea un combo box
        frame=ctk.CTkFrame(place, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(frame, text=text, font=("Arial", 12, "bold")).pack(side="top", anchor="w")

        #Creamos el combo bvox
        combo = ctk.CTkComboBox(frame, values=values, width=200,text_color="white",fg_color="#230b67", border_color="#230b67",button_color="#FFA600", button_hover_color="#CC8500")
        combo.pack(fill="x", pady=5)

        self.combos[key] = combo
        return combo

    def updateComboBoxImages(self):
        #FUnción para actualizar los combo box de imagenes
        nombres = list(self.openedImages.keys())

        if not nombres:
            nombres = ["No hay imágenes cargadas"]

        for combo in self.combos.values():
            current = combo.get()

            combo.configure(values=nombres)

            if current in nombres:
                combo.set(current)
            else:
                combo.set(nombres[0])

    def validateComboImage(self, comboImages, imageType="imagen"):

        #Obtener nombre del combo
        name = str(comboImages.get()).strip()

        #Validar selección
        if name=="No hay imágenes cargadas" or not name:
            messagebox.showwarning("Atención","Selecciona una "+str(imageType)+" válida en el menú desplegable")
            return None

        #Validar existencia en diccionario
        if name not in self.openedImages:
            messagebox.showerror("Error","La "+str(imageType)+" "+str(name)+" no se encuentra registrada")
            return None

        #Obtener imagen
        image = self.openedImages[name]

        # Validar imagen
        if image is None:
            messagebox.showwarning("Atención","La "+str(imageType)+" "+str(name)+" no se pudo cargar correctamente")
            return None

        return image
    
#PANEL DE BOTONES

    def createGridButton(self, place, icon, command, row, col, fg="#FFA600", hover="#CC8500"):
        #Función que crea botones cuadrados en una cuadrícula
        icon=self.loadIcon(icon, 35, 35)
        button=ctk.CTkButton(place, image=icon, text="",width=60, height=60,corner_radius=8, fg_color=fg,hover_color=hover, command=command)
        button.grid(row=row, column=col, padx=10, pady=10)
        button.image = icon
        return button

#CONTENEDOR PARA MENU
    def createContainer(self, menuPanel):
        #crear un container
        container=ctk.CTkFrame(menuPanel)
        container.pack(fill="both", expand=True)

        color = container._apply_appearance_mode(container._fg_color)

        canvas = tk.Canvas(container, highlightthickness=0, bg=color, bd=0)
        canvas.pack(side="left", fill="both", expand=True)

        #crear scroll
        scroll=ctk.CTkScrollbar(container, command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)

        self.scrollFrame = ctk.CTkFrame(canvas, fg_color="transparent")
        window =canvas.create_window((0, 0), window=self.scrollFrame, anchor="nw")

        #Configuramos el scroll cuando el frame cambia de tamaño
        self.scrollFrame.bind("<Configure>", lambda event: (canvas.update_idletasks(), canvas.configure(scrollregion=canvas.bbox("all"))))

        #Configuramos el ancho
        canvas.bind("<Configure>", lambda event: canvas.itemconfig(window, width=event.width))

        #Configuramos un scroll con el mouse
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda event: self.mouseWheel(canvas, event)))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        container.bind("<Destroy>", lambda e: canvas.unbind_all("<MouseWheel>"))

        canvas.update_idletasks()

    def mouseWheel(self, canvas, event):
        #Función para scrollear con el mouse
        if event.state & 0x0001:
            canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        else:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def resourcePath(self,relativePath):
        #Función para cargar recursos
        try:
            basePath = sys._MEIPASS
        except Exception:
            basePath = os.path.abspath(".")
        return os.path.join(basePath, relativePath)
