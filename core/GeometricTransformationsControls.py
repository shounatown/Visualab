import customtkinter as ctk
from tkinter import messagebox
from .ButtonsFunctionalities import ButtonsFunctionalities
from pdi.GeometricTransformations import GeometricTransformations
import tkinter as tk

class GeometricTransformationsControls(ButtonsFunctionalities):
    #GeometricTransformationsControls se encarga de configurar todos los controles de esta sección del menú

    def __init__(self, menuPanel, tabView, openedImages, createdTabs):
        #Constructor de la clase
        super().__init__(tabView, openedImages, createdTabs)
        self.menuPanel = menuPanel
        #Creamos los botones
        self.createControls()

    def createControls(self):
        #Esta función inicializa todos los botones

        #Creamos un contenedor
        self.createContainer(self.menuPanel)

        ####Para escalar####
        scalePanel=ctk.CTkFrame(self.scrollFrame, corner_radius=15, border_width=1)
        scalePanel.pack(fill="x", padx=10, pady=10)

        icon=self.loadIcon("assets/images/scale.png", 40, 40)
        labelScale=ctk.CTkLabel(scalePanel, image=icon, text="   Escalar", compound="left", font=("Roboto", 14, "bold"))
        labelScale.pack(side="top", anchor="nw", padx=10, pady=5)
        labelScale.image=icon

        #Radio buttons para elegir el modo
        self.scaleMode=ctk.StringVar(value="factor")

        rbPanel=ctk.CTkFrame(scalePanel, fg_color="transparent")
        rbPanel.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(rbPanel, text="Seleccione el modo:", font=("Roboto", 12, "bold")).pack(anchor="w")

        self.rbFactor = ctk.CTkRadioButton(rbPanel, text="Por factor", variable=self.scaleMode, value="factor",
                                        fg_color="#FFA600", hover_color="#CC8500")
        self.rbFactor.pack(anchor="w", pady=5)

        self.rbSize = ctk.CTkRadioButton(rbPanel, text="Por tamaño px",variable=self.scaleMode, value="size",
                                        fg_color="#FFA600", hover_color="#CC8500")
        self.rbSize.pack(anchor="w", pady=5)

        #Entradas de texto
        panelBox=ctk.CTkFrame(scalePanel, fg_color="transparent", corner_radius=8, border_width=0)
        panelBox.pack(fill="x", padx=10, pady=10)
        self.scaleX=self.createNumberBox(panelBox, "Ancho (X):", allowNegative=False)
        self.scaleY=self.createNumberBox(panelBox, "Alto (Y):", allowNegative=False)

        #Botón para ejecutar escala
        ctk.CTkButton(scalePanel, text="Aplicar Escala", command=self.applyScale,fg_color="#FFA600", hover_color="#CC8500", text_color="#FFFFFF"
        ).pack(fill="x", padx=20, pady=15)


        ####Para trasladar##
        self.transX, self.transY = self.createNumberPanel("Trasladar", "assets/images/move.png",["Trasladar X", "Trasladar Y"], self.applyTranslate)

        ####Para rotar####
        self.angleSlider=self.createSliderPanel("Rotación","assets/images/rotation.png", "Ángulo", 0, 360, self.applyRotate, last="°")

        ####Para reflexión####
        self.reflectOption = self.createRadioButtonPanel("Reflexión", "assets/images/reflect.png",[("Horizontal", "horizontal"), ("Vertical", "vertical")], self.applyReflect, "horizontal")


    def applyScale(self):
        #Función que aplica la escala
        image, name= self.getImage()
        if image is not None:
            mode=self.scaleMode.get()
            try:    #Tratamos de obtener los valores
                fx=float(self.scaleX.get())
                fy=float(self.scaleY.get())
                if fx <= 0 or fy <= 0:
                    messagebox.showwarning("Atención", "Los valores deben ser mayores a 0")    #Lanzar error si es 0  menor
                if "factor" in mode:
                    result = self.gt.scale(image, fx, fy)
                else:
                    result = self.gt.scalePX(image, int(fx), int(fy))
                self.showResult(result, name, "scale")
            except: #Si están mal enviamos advertencia
                messagebox.showerror("Error", "Valores inválidos en escala")
                return


    def applyTranslate(self):
        #Función que aplica la traslación
        image, name = self.getImage()
        if image is not None:
            try:    #Tratamos de obtener los valores
                tx=float(self.transX.get())
                ty=float(self.transY.get())
            except: #Si están mal enviamos advertencia
                messagebox.showerror("Error", "Valores inválidos en traslación")
                return
            result = self.gt.translate(image, tx, ty)
            self.showResult(result, name, "translate")

    def applyRotate(self):
        #Función que aplica la rotación
        image,name = self.getImage()
        if image is not None:
            angle=self.angleSlider.get()
            result=self.gt.rotate(image, angle)
            self.showResult(result, name, "rotate")

    def applyReflect(self):
        #Función que aplica la reflexión
        image, name = self.getImage()
        if image is not None:
            mode=self.reflectOption.get()
            result=self.gt.reflect(image, mode)
            self.showResult(result, name, "reflect")
