import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from .ButtonsFunctionalities import ButtonsFunctionalities

class ConnectivityControls(ButtonsFunctionalities):
    #Esta clase inicializa los botones para la sección de conectividad

    def __init__(self, menuPanel, tabView, openedImages, createdTabs):
        #Constructor
        super().__init__(tabView, openedImages, createdTabs)
        self.menuPanel = menuPanel

        #Construimos los controles
        self.createControls()

    def createControls(self):
        self.createContainer(self.menuPanel)
        self.scrollFrame.pack(fill="both", expand=True)

        #Panel para todo el contenido
        mainPanel = ctk.CTkFrame(self.scrollFrame, corner_radius=15, border_width=1)
        mainPanel.pack(fill="x", padx=10, pady=10)


        ctk.CTkLabel(mainPanel, text="Etiquetado de componentes", font=("Roboto", 12, "bold"), text_color="#000000").pack(pady=(15, 10))

        #Radio buttons para elegir la forma de visualización
        self.value=ctk.StringVar(value="etiquetas")
        radioButtons=ctk.CTkFrame(mainPanel, fg_color="transparent")
        radioButtons.pack(fill="x", padx=20, pady=5,  expand=True)

        ctk.CTkLabel(radioButtons, text="Modo de visualización:", font=("Roboto", 12, "bold")).pack(anchor="w")

        #Radio button colores
        self.rbColors = ctk.CTkRadioButton(radioButtons, text="ColorMap", variable=self.value, value="colores",
                                            fg_color="#FFA600", hover_color="#CC8500")
        self.rbColors.pack(anchor="w", pady=5)

        # Radio button etiquetas
        self.rbEtiquetas = ctk.CTkRadioButton(radioButtons, text="Etiquetas", variable=self.value, value="etiquetas",
                                            fg_color="#FFA600", hover_color="#CC8500")
        self.rbEtiquetas.pack(anchor="w", pady=5)

        #Seleccionar el tipo de vecindad
        ctk.CTkLabel(mainPanel, text="Seleccione el tipo de conectividad:", font=("Roboto", 12, "italic")).pack(pady=(15, 0))

        #Botones
        self.createIconButton("Vecindad 4", "assets/images/4connectivityr.png", lambda: self.applyConnectivity(4),
                        "#FFA600", "#CC8500", mainPanel)

        self.createIconButton("Vecindad 8", "assets/images/8connectivityr.png", lambda: self.applyConnectivity(8),
            "#FFA600", "#CC8500", mainPanel)

    def applyConnectivity(self, neighbour):
        #Obtener imagen
        image,name=self.getImage()

        #validar
        if image is None:
            messagebox.showwarning("Atención", "No hay ninguna imagen seleccionada")
            return

        #Obtener modo desde la variable del Radio Button
        value=self.value.get()

        try:
            #Aplicar dependiendo de la vecindad
            if value=="colores":
                result,count=self.conn.useColorMap(image, neighbour)
            if value=="etiquetas":
                result,count=self.conn.useLabels(image, neighbour)

            #Mostrar imagen
            if result is not None:
                self.showResult(result, name, str(value)+"_V"+str(neighbour))
            #Avisar cuantos objetos se encontraron
                if count==0:
                    messagebox.showinfo("Atención", "No se encontraron componentes en la imagen")
                else:
                    messagebox.showinfo("Éxito",str(count)+" objetos encontrados")
            else:
                messagebox.showerror("Error", "No se pudo procesar la imagen")

        except Exception as e:
            print(str(e))