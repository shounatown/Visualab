import customtkinter as ctk
from tkinter import messagebox
from .ButtonsFunctionalities import ButtonsFunctionalities

class ImageOperationsControls(ButtonsFunctionalities):
    #Esta clase crea los controles para las operaciones entre imágenes
    def __init__(self, menuPanel, tabView, openedImages, createdTabs):
        #Constructor
        super().__init__(tabView, openedImages, createdTabs)
        self.menuPanel = menuPanel

        #Creamos los controles
        self.createControls()

    def createControls(self):
        #Función para crear todos los controles de la sección operaciones entre imágenes
        self.createContainer(self.menuPanel)

        self.comboPanel = ctk.CTkFrame(self.scrollFrame, corner_radius=15, border_width=1)
        self.comboPanel.pack(fill="x", padx=10, pady=10)

        #Creamos un combo box despegable
        if self.openedImages:
            images=list(self.openedImages.keys())
        else:
            images=["No hay imágenes cargadas"]

        if self.tabView.get()!="Inicio":
            currentImage = "Imagen actual"
        else:
            currentImage = "Ninguna"
        ctk.CTkLabel(self.comboPanel, text="Imagen 1: "+str(currentImage), font=("Roboto", 12, "bold")).pack(pady=(15, 0))
        self.comboImages=self.createComboBoxImages("images", self.comboPanel, "Selecciona la imagen 2:", images)

        ####Botones de operaciones aritmetricas
        ctk.CTkLabel(self.scrollFrame, text="Operaciones aritméticas",font=("Roboto", 12, "bold")).pack(pady=(15, 0))

        #Penel cuadrículado
        aritmeticPanel=ctk.CTkFrame(self.scrollFrame, fg_color="transparent")
        aritmeticPanel.pack(pady=15)

        #Fila 0:
        self.additionButton=self.createGridButton(aritmeticPanel,"assets/images/additionr.png",lambda: self.applyOperation("addition"), 0, 0)
        self.substractionButton=self.createGridButton(aritmeticPanel,"assets/images/substractionr.png",lambda: self.applyOperation("subtraction"), 0, 1)

        #Fila 1:
        self.multiplicationButton=self.createGridButton(aritmeticPanel,"assets/images/multiplyr.png",lambda: self.applyOperation("multiplication"), 1, 0)
        self.divisionButton=self.createGridButton(aritmeticPanel,"assets/images/divisionr.png",lambda: self.applyOperation("division"), 1, 1)

        ####Botones de operaciones lógicas
        ctk.CTkLabel(self.scrollFrame, text="Operaciones lógicas",font=("Roboto", 12, "bold")).pack(pady=(15, 0))

        #Penel cuadrículado
        logicPanel=ctk.CTkFrame(self.scrollFrame, fg_color="transparent")
        logicPanel.pack(pady=15)

        #Fila 0:
        self.btnAnd = self.createGridButton(logicPanel, "assets/images/andr.png", lambda: self.applyOperation("and"), 0, 0)
        self.btnOr = self.createGridButton(logicPanel, "assets/images/orr.png", lambda: self.applyOperation("or"), 0, 1)

        #Fila 1:
        self.btnXor = self.createGridButton(logicPanel, "assets/images/xorr.png", lambda: self.applyOperation("xor"), 0, 2)

    def applyOperation(self, operation):
        #Función para aplicar la operación entre dos imágenes
        #Obtener Imagen A
        imageA, nameA = self.getImage()
        if imageA is None:
            return

        #Obtener Imagen B
        imageB = self.validateComboImage(self.comboImages, "imagen B")
        if imageB is None:
            return

        #Obtener nombre de imagen B
        nameB = str(self.comboImages.get()).strip()

        #Compatibilidad de canales
        newImageA, newImageB = self.io.matchChannels(imageA, imageB)

        if newImageA is None:
            return

        #Compatibilidad de tamaño
        newImageA, newImageB = self.io.matchSize(newImageA, newImageB)

        if newImageA is None:
            return

        #Operaciones
        try:
            if operation=="addition":
                result = self.io.addition(newImageA, newImageB)
            elif operation=="subtraction":
                result=self.io.subtraction(newImageA, newImageB)
            elif operation == "multiplication":
                result = self.io.multiplication(newImageA, newImageB)
            elif operation== "division":
                result = self.io.division(newImageA, newImageB)
            elif operation == "and":
                result = self.io.AND(newImageA, newImageB)
            elif operation == "or":
                result = self.io.OR(newImageA, newImageB)
            elif operation == "xor":
                result = self.io.XOR(newImageA, newImageB)

            self.showResult(result, nameA, operation+"_"+nameB)
        except Exception as e:
            messagebox.showerror("Error de Operación", "No se pudo realizar la operación"+str(operation)+": "+str(e))