import customtkinter as ctk
from tkinter import messagebox
from .ButtonsFunctionalities import ButtonsFunctionalities


class BasicOperationsControls(ButtonsFunctionalities):
    #Esta clase crea los controles para las operaciones básicas
    def __init__(self, menuPanel, tabView, openedImages, createdTabs):
        #Constructor
        super().__init__(tabView, openedImages, createdTabs)
        self.menuPanel = menuPanel

        #Creamos los controles
        self.createControls()

    def createControls(self):
        #Función para crear los controles

        #Inicializamos el contenedor de scroll
        self.createContainer(self.menuPanel)

        ####Para el negativo####
        self.createIconButton("Aplicar negativo", "assets/images/notr.png", self.applyNegative,"#FFA600", "#CC8500", self.scrollFrame)

        ####Para el umbralizado####
        self.umbralSlider=self.umbralSlider = self.createSliderPanel( "Umbralizar", "assets/images/umbral.png", "Umbral", 0,255,self.applyUmbralize, "")

        #Etiqueta de la operaciones con escalar
        ctk.CTkLabel(self.scrollFrame, text="Operaciones con escalar", font=("Roboto", 12, "bold")).pack(pady=(15, 5))

        ####Operaciones con escalar####
        self.additionSlider = self.createSliderPanel("Suma", "assets/images/addition.png", "Valor",0, 255, self.applyAddition)
        self.subtractionSlider = self.createSliderPanel("Resta", "assets/images/subtraction.png","Valor", 0, 255, self.applySubtraction)
        self.multiplySlider = self.createSliderPanel("Multiplicación", "assets/images/multiply.png","Valor",  0, 255, self.applyMultiplication)
        self.divisionSlider = self.createSliderPanel("División", "assets/images/division.png","Valor",  1, 255, self.applyDivision)

    def applyNegative(self):
        #Función que aplica el negativo a la imagen
        image,name=self.getImage()
        if image is not None:
            #Llamamos a la función y mostramos el resultado
            result =self.bo.negative(image)
            self.showResult(result, name, "negative")

    def applyUmbralize(self):
        #Función que aplica el umbralizado a la imagen
        image,name=self.getImage()
        if image is not None:
            #Llamamos a la función y mostramos el resultado
            value=self.umbralSlider.get() #Valor del umbral
            result=self.bo.umbralize(image, value)
            self.showResult(result, name, "threshold")

    def applyAddition(self):
        #Función que aplica la suma a la imagen
        image, name = self.getImage()
        if image is not None:
            #Llamamos a la función y mostramos el resultado
            value= self.additionSlider.get() #Valor
            result=self.bo.scalarAddition(image, value)
            self.showResult(result, name, "addition")

    def applySubtraction(self):
        #Función que aplica la resta a la imagen
        image,name = self.getImage()
        if image is not None:
            #Llamamos a la función y mostramos el resultado
            value=self.subtractionSlider.get()
            result=self.bo.scalarSubtraction(image, value)
            self.showResult(result, name, "subtraction")

    def applyMultiplication(self):
        #Función que aplica la multiplicación a la imagen
        image, name = self.getImage()
        if image is not None:
            #Llamamos a la función y mostramos el resultado
            value = self.multiplySlider.get()#Valor
            result = self.bo.scalarMultiplication(image, value)
            self.showResult(result, name, "multiplication")

    def applyDivision(self):
        #Función que aplica la división a la imagen
        image,name=self.getImage()
        if image is not None:
            #Llamamos a la función y mostramos el resultado
            value=self.divisionSlider.get() #Valor
            if value==0:
                value=1 #Evitar división por cero
            result = self.bo.scalarDivision(image, value)
            self.showResult(result, name, "division")