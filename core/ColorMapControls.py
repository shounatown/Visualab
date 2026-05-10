import customtkinter as ctk
from tkinter import messagebox, colorchooser
from .ButtonsFunctionalities import ButtonsFunctionalities

class ColorMapControls(ButtonsFunctionalities):
    def __init__(self, menuPanel, tabView, openedImages, createdTabs):
        super().__init__(tabView, openedImages, createdTabs)
        self.menuPanel = menuPanel
        self.selected_colors = [] # Lista para almacenar tuplas BGR
        self.createControls()
        self.cm.loadNewMaps()

    def createControls(self):
        #Botón Escala de Grises
        ctk.CTkButton(self.menuPanel, text="Cambiar a escala de grises", fg_color="#FFA600",command=self.applyGrayScale, text_color="white").pack(fill="x", padx=15, pady=20)

        ####SELECCIONA UN COLOR####
        ctk.CTkLabel(self.menuPanel, text="Selecciona un mapa de color:").pack(pady=5)

        values = list(self.cm.maps.keys())+list(self.cm.newMaps.keys())
        #Menú desplegable (OptionMenu)
        self.defaultMaps = ctk.CTkOptionMenu(self.menuPanel,values=values,command=lambda v: self.updatePreview(v),
            fg_color="#28066B", button_color="#28066B", button_hover_color="#3D09A1",text_color="white"
        )
        self.defaultMaps.pack(fill="x", padx=15, pady=5)

        #Vista previa
        self.previewLabel=ctk.CTkLabel(self.menuPanel, text="")
        self.previewLabel.pack(pady=10)
        self.updatePreview(self.defaultMaps.get())

        #Botón Aplicar
        ctk.CTkButton(self.menuPanel, text="Aplicar mapa", fg_color="#FFA600", text_color="white",command=lambda: self.applyColorMap(self.defaultMaps)).pack(fill="x", padx=15, pady=10)

        ####NUEVO MAPA PERSONALIZADO####
        ctk.CTkLabel(self.menuPanel, text="Crea un mapa de color personalizado:").pack(pady=5)
        #Botón crear nuevo mapa
        ctk.CTkButton(self.menuPanel, text="Crear nuevo mapa", fg_color="#FFA600", text_color="white",command=lambda: self.createColorMap(self.defaultMaps)).pack(fill="x", padx=15, pady=10)


    def applyGrayScale(self):
        #Función para aplicar una escala de grises a la imagen
        image, name=self.getImage()
        if image is not None:
            #Aplicamos los grises si hay una imagen
            result=self.cm.applyGrayScale(image)
            self.showResult(result, name, "grayscale")

    def applyColorMap(self, optionMenu):
        #Función para aplicar una mapa de color a la imagen
        image,name=self.getImage()
        if image is not None:
            #Aplicamos el mapa si hay una imagen
            selected=optionMenu.get()
            #Primero pasamos a grises la imagen
            gray=self.cm.applyGrayScale(image)
            #Luego aplicamos el mapa
            result=self.cm.applyColorMap(gray, selected)
            self.showResult(result, name, selected)

    def updatePreview(self, colorMap):
        #FUnción para actualizar la vista previa del color map
        preview=self.cm.colorMapPreview(colorMap)
        image=self.cv2ToCTK(preview)
        self.previewLabel.configure(image=image)
        self.previewLabel.image=image

    def createColorMap(self, optionMenu):
        #Función para crear una ventana emergente para elegir los colores
        self.windowColors=ctk.CTkToplevel(self.menuPanel)
        self.windowColors.title("Crear color map personalizado")
        self.windowColors.geometry("400x500")
        self.windowColors.grab_set() #Para bloquear la app principal hasta cerrar esta

        self.selectedColors=[] #Lista de colores elegidos en bgr

        ctk.CTkLabel(self.windowColors, text="Colores del mapa", font=("Roboto", 16, "bold")).pack(pady=10)

        #Contenedor de la lista de colores
        self.colorsPanel=ctk.CTkScrollableFrame(self.windowColors, height=200)
        self.colorsPanel.pack(fill="x", padx=20, pady=5)

        #Botones
        buttons=ctk.CTkFrame(self.windowColors, fg_color="transparent")
        buttons.pack(pady=10)

        ctk.CTkButton(buttons, text="Agregar color", width=100, fg_color="#28066B", command=self.addColor).pack(side="left", padx=5)

        ctk.CTkButton(buttons, text="Limpiar", width=100, fg_color="#CC0000", command=self.clear).pack(side="left", padx=5)

        #Nombre del mapa
        ctk.CTkLabel(self.windowColors, text="Nombre del mapa:").pack()
        self.mapName=ctk.CTkEntry(self.windowColors, placeholder_text="Escribe un nombre")
        self.mapName.pack(fill="x", padx=40, pady=10)

        #Botón para guardar
        ctk.CTkButton(self.windowColors, text="Guardar mapa de color", fg_color="#FFA600", text_color="black", command=lambda: self.saveColorMap(optionMenu)).pack(pady=20)

    def addColor(self):
        #Función para agregar un color a el mapa
        selected=colorchooser.askcolor(title="Selecciona un color para tu mapa")


        #Si se ha seleccionado un color
        if selected and selected[0]:
            r, g, b=selected[0]
            HEXcolor=selected[1]

            #Guardamos en bgr
            rgb=(float(int(r)/255),float(int(g)/255),float(int(b)/255))
            self.selectedColors.append(rgb)

            #Par pintar los nombres
            luz=(0.3*r+0.59*g+0.11*b)/255
            if luz>0.5:
                text="#000000"
            else:
                text="#FFFFFF"

            #Etiqueta del color
            label=ctk.CTkLabel(self.colorsPanel,text="Color "+str(len(self.selectedColors))+": "+HEXcolor,fg_color=HEXcolor,
                                text_color=text,height=28,corner_radius=5)
            label.pack(fill="x", pady=3, padx=5)

    def clear(self):
        #Función para limpiar los colores
        self.selectedColors=[]
        for color in self.colorsPanel.winfo_children():
            color.destroy()

    def saveColorMap(self, optionMenu):
        #Función para guardar los colores
        name=self.mapName.get().strip()
        if not name or len(self.selectedColors)<2:
            messagebox.showwarning("Error", "Necesitas nombar el mapa y agregar al menos 2 colores")
            return

        #Guardar color map
        self.cm.saveNewColorMap(name, self.selectedColors)

        #Actualizar el combo box
        comboBox=list(self.cm.maps.keys())+list(self.cm.newMaps.keys())
        optionMenu.configure(values=comboBox)
        optionMenu.set(name)
        self.updatePreview(name)

        #Cerrar ventana
        self.windowColors.destroy()
        messagebox.showinfo("Éxito", "ColorMap "+str(name)+" ha sido guardado")
