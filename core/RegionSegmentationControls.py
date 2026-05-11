import customtkinter as ctk
from tkinter import messagebox
from .ButtonsFunctionalities import ButtonsFunctionalities
from .ImageOperationsControls import ImageOperationsControls
import cv2
import numpy as np

class RegionSegmentationControls(ButtonsFunctionalities):
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

        #########################1 Se convierte a HSV#########################
        self.createIconButton("Cambiar espacio de color a HSV", "assets/images/hsv.png", self.changeTohsv,"#28066B", "#3D09A1", self.scrollFrame)

        #########################2 Ecualizacion normal#########################
        self.createIconButton("Aplicar ecualización normal", "assets/images/normalEcualization.png", self.applyNormalEcualization,"#28066B", "#3D09A1", self.scrollFrame)

        #########################3 Unir HSV#########################

        #Creamos un combo box despegable
        if self.openedImages:
            images=list(self.openedImages.keys())
        else:
            images=["No hay imágenes cargadas"]

        self.comboPanel = ctk.CTkFrame(self.scrollFrame, corner_radius=15, border_width=1)
        self.comboPanel.pack(fill="x", padx=10, pady=10)
        self.comboH = self.createComboBoxImages("H", self.comboPanel, "Canal H", images)
        self.comboS = self.createComboBoxImages("S", self.comboPanel, "Canal S", images)
        self.comboV = self.createComboBoxImages("V", self.comboPanel, "Canal V", images)

        ctk.CTkButton(self.comboPanel,text="Unir canales HSV",fg_color="#FFA600",
                    command=lambda: self.joinHSVChannels()).pack(fill="x", padx=15, pady=20)


        #########################4 Gaussian blur#########################
        blurPanel=ctk.CTkFrame(self.scrollFrame, corner_radius=15, border_width=1)
        blurPanel.pack(fill="x", padx=10, pady=10)

        icon=self.loadIcon("assets/images/blur.png", 40, 40) # Asegúrate de tener este icono
        labelBlur=ctk.CTkLabel(blurPanel, image=icon, text="   Filtro de gaussiano",compound="left", font=("Roboto", 14, "bold"))
        labelBlur.pack(side="top", anchor="nw", padx=10, pady=5)
        labelBlur.image = icon
        #Slider
        self.kernelLabelB=ctk.CTkLabel(blurPanel, text="Tamaño del Kernel: 5x5")
        self.kernelLabelB.pack(pady=(10, 0))
        self.sliderKernelB=ctk.CTkSlider(blurPanel, from_=1, to=51, number_of_steps=25,command=lambda v: self.updateSliderFG(v,self.kernelLabelB))
        self.sliderKernelB.set(5)
        self.sliderKernelB.pack(fill="x", padx=20, pady=5)
        #Botón
        ctk.CTkButton(blurPanel, text="Aplicar filtro gaussiano",command=self.applyGaussianBlur, 
                    fg_color="#FFA600", hover_color="#CC8500", text_color="#FFFFFF").pack(fill="x", padx=20, pady=15)

        #########################5 Umbralización por canales HSV#########################
        self.createIconButton("Umbralizado por canales HSV", "assets/images/umbralr.png", self.umbralHSVWindow,"#28066B", "#3D09A1", self.scrollFrame)

        #########################6 Operaciones lógicas#########################
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
        self.comboImages=self.createComboBoxImages("imagesLogic", self.comboPanel, "Selecciona la imagen 2:", images)

        ####Botones de operaciones lógicas
        ctk.CTkLabel(self.scrollFrame, text="Operaciones lógicas",font=("Roboto", 12, "bold")).pack(pady=(15, 0))

        #Penel cuadrículado
        logicPanel=ctk.CTkFrame(self.scrollFrame, fg_color="transparent")
        logicPanel.pack(pady=15)

        #Fila 0:
        self.btnAnd = self.createGridButton(logicPanel, "assets/images/andr.png", lambda: self.applyOperation("and"), 0, 0)
        self.btnOr = self.createGridButton(logicPanel, "assets/images/orr.png", lambda: self.applyOperation("or"), 0, 1)

        #Fila 1:
        self.btnNot = self.createGridButton(logicPanel, "assets/images/notr.png", lambda: self.applyOperation("not"), 0, 2)

        #########################7 Filtrado máximos y mínimos#########################
        maxMinPanel=ctk.CTkFrame(self.scrollFrame, corner_radius=15, border_width=1)
        maxMinPanel.pack(fill="x", padx=10, pady=10)

        icon=self.loadIcon("assets/images/maxmin.png", 40, 40)
        labelMaxMin=ctk.CTkLabel(maxMinPanel, image=icon, text="   Filtrado MIN-MAX",compound="left", font=("Roboto", 14, "bold"))
        labelMaxMin.pack(side="top", anchor="nw", padx=10, pady=5)
        labelMaxMin.image = icon

        #Slider
        self.kernelLabelMaxMin=ctk.CTkLabel(maxMinPanel, text="Tamaño del Kernel: 5x5")
        self.kernelLabelMaxMin.pack(pady=(10, 0))

        self.sliderKernelMaxMin=ctk.CTkSlider(maxMinPanel, from_=1, to=51, number_of_steps=25,command=lambda v: self.updateSliderFG(v, self.kernelLabelMaxMin))
        self.sliderKernelMaxMin.set(5)
        self.sliderKernelMaxMin.pack(fill="x", padx=20, pady=5)

        #NumberBox
        panelBoxF=ctk.CTkFrame(maxMinPanel, fg_color="transparent", corner_radius=8, border_width=0)
        panelBoxF.pack(fill="x", pady=10)
        self.iteraciones = self.createNumberBox(panelBoxF, "Iteraciones:", allowNegative=False)

        #Botón
        ctk.CTkButton(maxMinPanel, text="Filtrar",command=self.applyMaxMin,
                    fg_color="#FFA600", hover_color="#CC8500", text_color="#FFFFFF").pack(fill="x", padx=20, pady=15)
        
        #########################8 Filtrado mediana#########################
        medianPanel=ctk.CTkFrame(self.scrollFrame, corner_radius=15, border_width=1)
        medianPanel.pack(fill="x", padx=10, pady=10)

        icon=self.loadIcon("assets/images/median.png", 40, 40) # Asegúrate de tener este icono
        labelMedian=ctk.CTkLabel(medianPanel, image=icon, text="   Filtro de la mediana",compound="left", font=("Roboto", 14, "bold"))
        labelMedian.pack(side="top", anchor="nw", padx=10, pady=5)
        labelMedian.image = icon
        #Slider
        self.kernelLabelMedian=ctk.CTkLabel(medianPanel, text="Tamaño del Kernel: 5x5")
        self.kernelLabelMedian.pack(pady=(10, 0))
        self.sliderKernelMedian=ctk.CTkSlider(medianPanel, from_=1, to=51, number_of_steps=25,command=lambda v: self.updateSliderFG(v, self.kernelLabelMedian))
        self.sliderKernelMedian.set(5)
        self.sliderKernelMedian.pack(fill="x", padx=20, pady=5)
        #Botón
        ctk.CTkButton(medianPanel, text="Aplicar filtro de la mediana",command=self.applyMedian, 
                    fg_color="#FFA600", hover_color="#CC8500", text_color="#FFFFFF").pack(fill="x", padx=20, pady=15)

        #########################9 Morfología Matematica#########################
        morphologyPanel=ctk.CTkFrame(self.scrollFrame, corner_radius=15, border_width=1)
        morphologyPanel.pack(fill="x", padx=10, pady=10)

        icon=self.loadIcon("assets/images/morph.png", 40, 40)

        labelMorph=ctk.CTkLabel( morphologyPanel,image=icon,text="   Morfología matemática",compound="left",font=("Roboto", 14, "bold"))
        labelMorph.pack(side="top", anchor="nw", padx=10, pady=5)
        labelMorph.image = icon

        #Slider EE
        self.kernelLabelMorph=ctk.CTkLabel(morphologyPanel,text="EE: 5x5")

        self.kernelLabelMorph.pack(pady=(10,0))

        self.sliderKernelMorph=ctk.CTkSlider(morphologyPanel, from_=1,to=51, number_of_steps=25,
            command=lambda v: self.updateSliderFG(v, self.kernelLabelMorph))

        self.sliderKernelMorph.set(5)
        self.sliderKernelMorph.pack(fill="x", padx=20, pady=5)

        #Iteraciones
        panelBoxMorph=ctk.CTkFrame(morphologyPanel,fg_color="transparent")
        panelBoxMorph.pack(fill="x", pady=10)

        self.iteracionesMorph = self.createNumberBox(panelBoxMorph,"Iteraciones:",allowNegative=False)


        #Cuadricula de los botones
        morphPanel=ctk.CTkFrame(morphologyPanel,fg_color="transparent")
        morphPanel.pack(pady=10)

        # Fila 1
        self.btnDilate = self.createGridButton(morphPanel,"assets/images/dilate.png",lambda: self.applyMM("dilate"),0, 0, "#28066B", "#3D09A1",)
        self.btnErode = self.createGridButton(morphPanel,"assets/images/erode.png",lambda: self.applyMM("erode"),0,1,"#28066B", "#3D09A1",)

        # Fila 2
        self.btnOpen = self.createGridButton(morphPanel, "assets/images/opening.png",lambda: self.applyMM("open"),1,0,"#28066B", "#3D09A1",)
        self.btnClose = self.createGridButton(morphPanel,"assets/images/closing.png",lambda: self.applyMM("close"),1,1,"#28066B", "#3D09A1",)

        #########################10 CONTORNOS#########################
        contoursPanel=ctk.CTkFrame(self.scrollFrame, corner_radius=15, border_width=1)
        contoursPanel.pack(fill="x", padx=10, pady=10)

        icon=self.loadIcon("assets/images/contours.png", 40, 40)

        labelContours=ctk.CTkLabel(contoursPanel,image=icon,text="   Obtener contornos",compound="left",font=("Roboto", 14, "bold"))

        labelContours.pack(side="top", anchor="nw", padx=10, pady=5)
        labelContours.image = icon

        #Combo máscaras
        if self.openedImages:
            images=list(self.openedImages.keys())
        else:
            images=["No hay imágenes cargadas"]

        self.comboMaskContours = self.createComboBoxImages("maskContours",contoursPanel,"Selecciona la máscara:",images)

        #Botón
        ctk.CTkButton(contoursPanel,text="Detectar objetos",command=self.applyContours,fg_color="#FFA600",hover_color="#CC8500",text_color="#FFFFFF").pack(fill="x", padx=20, pady=15)


        ######################### SEGMENTACIÓN #########################

        segmentationPanel = ctk.CTkFrame(self.scrollFrame, corner_radius=15, border_width=1)
        segmentationPanel.pack(fill="x", padx=10, pady=10)

        #FLOR
        ctk.CTkLabel(segmentationPanel,text="Segmentación de flor",font=("Roboto", 14, "bold")).pack(pady=10)
        ctk.CTkButton(segmentationPanel,text="Segmentar flor con MAX-MIN", fg_color="#7B2CBF",hover_color="#5A189A",command=self.applySegmentationMaxMin).pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(segmentationPanel,text="Segmentar flor con MM",fg_color="#7B2CBF",hover_color="#5A189A", command=self.applySegmentationMM).pack(fill="x", padx=20, pady=10)

        #PISTILO
        ctk.CTkLabel(segmentationPanel,text="Segmentación del pistilo",font=("Roboto", 14, "bold")).pack(pady=10)
        ctk.CTkButton(segmentationPanel,text="Segmentar pistilo con MM", fg_color="#7B2CBF",hover_color="#5A189A",command=self.applySegmentationPistilo).pack(fill="x", padx=20, pady=10)
        







    def changeTohsv(self):
        #Función que cambiar el espacio de color de rgb a hsv
        image,name=self.getImage()
        if image is not None:
            #Llamamos a la función y mostramos el resultado
            h,s,v =self.colorModels.rgbTohsv(image)
            self.showResult(h, name, "H")
            self.showResult(s, name, "S")
            self.showResult(v, name, "V")

    def applyNormalEcualization(self):
        #Función que aplica la ecualización normal
        image,name=self.getImage()
        if image is not None:
            #Llamamos a la función y mostramos el resultado
            result =self.ec.normalEcualization(image)
            self.showResult(result, name, "normalEcualization")

    def applyGaussianBlur(self):
        #Función para aplicar el filtro gaussiano
        #obtener imagen actual
        image, name = self.getImage()
        if image is not None:
            kernel = int(self.sliderKernelB.get())
            if kernel % 2 == 0:
                kernel += 1 # Asegurar que sea impar
            sigma=0
            result=self.noise.gaussianBlur(image, kernel, sigma)
            self.showResult(result, name, "filtro_gaussiano")

    def joinHSVChannels(self):
        #Función unir los canales HSV
        imageH = self.validateComboImage(self.comboH, "imagen H")
        if imageH is None:
            return

        imageS = self.validateComboImage(self.comboS, "imagen S")
        if imageS is None:
            return

        imageV = self.validateComboImage(self.comboV, "imagen V")
        if imageV is None:
            return

        #Ajustar el tamaño de los 3 canales
        imageH, imageS = self.io.matchSize(imageH, imageS)
        if imageH is None:
            return

        imageH, imageV = self.io.matchSize(imageH, imageV)
        if imageH is None:
            return

        imageS, imageV = self.io.matchSize(imageS, imageV)
        if imageS is None:
            return

        #Unir canales
        result=self.colorModels.joinHSV(imageH, imageS, imageV)
        self.showResult(result, "HSV.png", "joined")

    def umbralHSVWindow(self):
    #Función para abrir la ventana de umbralizado HSV
        image, name = self.getImage()

        if image is None:
            return

        self.u.openHSVWindow(image,name,self.showResult)

    def applyOperation(self, operation):
        #Función para aplicar la operación entre dos imágenes
        #Obtener Imagen A
        imageA, nameA = self.getImage()
        if imageA is None:
            return

        if operation != "not":
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
            if operation == "and":
                result = self.io.AND(newImageA, newImageB)
            elif operation == "or":
                result = self.io.OR(newImageA, newImageB)
            elif operation == "not":
                result = self.bo.negative(imageA)
                self.showResult(result, nameA, operation)
                return

            self.showResult(result, nameA, operation+"_"+nameB)
        except Exception as e:
            messagebox.showerror("Error de Operación", "No se pudo realizar la operación"+str(operation)+": "+str(e))

    def applyMaxMin(self):
        #Aplicar filtrado con maximos y minimos
        #Obtener imagen actual
        image, name = self.getImage()
        if image is None:
            return

        #Kernel y asegurar que sea impar
        kernel = int(self.sliderKernelMaxMin.get())
        if kernel % 2 == 0:
            kernel += 1

        #Iteraciones del numberBox
        try:
            iterations = int(self.iteraciones.get())
        except:
            iterations = 1

        #Asegurar mínimo 1 iteración
        iterations = max(1, iterations)

        result = image.copy()

        #Filtrado MIN-MAX en cadena
        for i in range(iterations):
            result = self.pba.filtroMinimo(result, kernel)
            result = self.pba.filtroMaximo(result, kernel)

        # Mostrar resultado
        self.showResult(result, name, "minmax")

    def updateSliderFG(self, value, label):
        #Función para actualizar la etiqueta del slider filtro gaussiano
        k=int(value)
        if k%2==0:#Solo impares
            k+=1
        label.configure(text="Tamaño del Kernel: "+str(k)+"x"+str(k))

    def applyMedian(self):
        #Función para aplicar el filtro de la mediana
        #Obtener imagen
        image, name = self.getImage()
        if image is None:
            return

        #Kernel del slider  impar
        kernel = int(self.sliderKernelMedian.get())
        if kernel % 2 == 0:
            kernel += 1

        #Aplicar filtro de mediana
        try:
            result = self.pba.medianBlur(image, kernel)
            self.showResult(result, name, "median_filter")
        except Exception as e:
            messagebox.showerror("Error en filtro mediana","No se pudo aplicar el filtro")

    def applyMM(self, operation):
        #Función para aplicar la MM
        # Obtener imagen
        image, name = self.getImage()
        if image is None:
            return

        #Kernel impar
        kernel = int(self.sliderKernelMorph.get())

        if kernel % 2 == 0:
            kernel += 1

        #Iteraciones
        try:
            iterations = int(self.iteracionesMorph.get())
        except:
            iterations = 1

        iterations = max(1, iterations)

        #Crear EE 
        ee = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel, kernel) )

        try:
            if operation == "dilate":
                result = self.mm.dilate(image, ee, iterations)
            elif operation == "erode":
                result = self.mm.erode(image, ee, iterations)
            elif operation == "open":
                result = self.mm.open(image, ee, iterations)
            elif operation == "close":
                result = self.mm.close(image, ee, iterations)

            self.showResult(result, name, operation)

        except Exception as e:
            messagebox.showerror("Error morfológico",str(e))

    def applyContours(self):
        #Funcion para aplicar contornos
        #imgen original
        image, name = self.getImage()

        if image is None:
            return

        #Máscara
        mask = self.validateComboImage(self.comboMaskContours,"máscara")
        #Convertir a gris si tiene 3 canales
        if len(mask.shape) == 3:
            mask= cv2.cvtColor(mask ,cv2.COLOR_BGR2GRAY)

        #Asegurar que es binaria
        _, mask  = cv2.threshold( mask,127,255,cv2.THRESH_BINARY)
        mask = mask.astype(np.uint8)


        if mask is None:
            return

        try:
            result = self.conn.getContoursWithMask(image,mask)
            self.showResult( result,name,"contours")

        except Exception as e:
            messagebox.showerror("Error contornos",str(e) )
            print(e)

    def applySegmentationMaxMin(self):
        image, name = self.getImage()
        if image is None:
            return

        try:
            result, mask, contours = self.seg.florByMaxMin(image, self.pba.filtroMinimo, self.pba.filtroMaximo,  self.conn)

            self.showResult(result, name, "flor_maxmin")
            self.showResult(mask, name, "mask_maxmin")
            self.showResult(contours, name, "contours_maxmin")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def applySegmentationMM(self):
        image, name = self.getImage()
        if image is None:
            return

        try:
            result, mask, contours = self.seg.florByMM(image, self.conn)

            self.showResult(result, name, "flor_mm")
            self.showResult(mask, name, "mask_mm")
            self.showResult(contours, name, "contours_mm")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def applySegmentationPistilo(self):
        image, name = self.getImage()
        if image is None:
            return

        try:
            result, mask, contours = self.seg.pistiloByMM(image, self.conn)

            self.showResult(result, name, "pistilo_mm")
            self.showResult(mask, name, "mask_pistilo")
            self.showResult(contours, name, "contours_pistilo")

        except Exception as e:
            messagebox.showerror("Error", str(e))