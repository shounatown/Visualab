import customtkinter as ctk
from tkinter import messagebox
from .ButtonsFunctionalities import ButtonsFunctionalities

class NoiseControls(ButtonsFunctionalities):
    #NoiseControls se encarga de configurar todos los controles de esta sección del menú

    def __init__(self, menuPanel, tabView, openedImages, createdTabs):
        #Constructor
        super().__init__(tabView, openedImages, createdTabs)
        self.menuPanel = menuPanel
        #Creamos los botones
        self.createControls()

    def createControls(self):
        #Función que crea los controles
        self.createContainer(self.menuPanel)

        ctk.CTkLabel(self.scrollFrame, text="Agregar ruido",font=("Roboto", 12, "bold")).pack(pady=(15, 0))

        ####Para Ruido gaussiano####
        gaussPanel=ctk.CTkFrame(self.scrollFrame, corner_radius=15, border_width=1)
        gaussPanel.pack(fill="x", padx=10, pady=10)
        icon=self.loadIcon("assets/images/gaussiano.png", 40, 40)
        labelGauss=ctk.CTkLabel(gaussPanel, image=icon, text="   Ruido gaussiano", compound="left", font=("Roboto", 14, "bold"))
        labelGauss.pack(side="top", anchor="nw", padx=10, pady=5)
        labelGauss.image=icon

        #Entradas de texto
        panelBoxG=ctk.CTkFrame(gaussPanel, fg_color="transparent", corner_radius=8, border_width=0)
        panelBoxG.pack(fill="x", padx=10, pady=10)
        self.muGauss=self.createNumberBox(panelBoxG, "Media (μ):", allowNegative=False)
        self.sigmaGauss=self.createNumberBox(panelBoxG, "Desviación (σ):", allowNegative=False)

        #Botón para ejecutar escala
        ctk.CTkButton(gaussPanel, text="Agregar ruido gaussiano", command=self.applyGauss,fg_color="#FFA600", hover_color="#CC8500", text_color="#FFFFFF"
        ).pack(fill="x", padx=20, pady=15)

        ####Ruido sal y pimienta##
        spPanel=ctk.CTkFrame(self.scrollFrame, corner_radius=15, border_width=1)
        spPanel.pack(fill="x", padx=10, pady=10)
        icon=self.loadIcon("assets/images/sp.png", 40, 40)
        labelSP=ctk.CTkLabel(spPanel, image=icon, text="   Ruido sal y pimienta", compound="left", font=("Roboto", 14, "bold"))
        labelSP.pack(side="top", anchor="nw", padx=10, pady=5)
        labelSP.image=icon

        #Sliders
        cantidadLabel= ctk.CTkLabel(spPanel, text="Cantidad: 50%")
        cantidadLabel.pack()
        self.sliderCantidad = ctk.CTkSlider(spPanel, from_=0, to=100, command=lambda v: self.updateSlider(v, cantidadLabel, "Cantidad", "%"))
        self.sliderCantidad.pack(fill="x", padx=20, pady=5)

        porcentajeLabel= ctk.CTkLabel(spPanel, text="Sal: 50% ---- Pimienta: 50%")
        porcentajeLabel.pack()
        self.sliderPorcentaje = ctk.CTkSlider(spPanel, from_=0, to=100, command=lambda v: self.updateSliderSP(v, porcentajeLabel))
        self.sliderPorcentaje.pack(fill="x", padx=20, pady=5)

        # Botón de Aplicar
        ctk.CTkButton(spPanel, text="Aplicar ruido sal y pimienta", fg_color="#FFA600",hover_color="#CC8500", command=self.applySaltAndPepper).pack(pady=10, padx=20, fill="x")

        ####Ruido speckle####
        specklePanel=ctk.CTkFrame(self.scrollFrame, corner_radius=15, border_width=1)
        specklePanel.pack(fill="x", padx=10, pady=10)
        icon=self.loadIcon("assets/images/speckle.png", 40, 40)
        labelSpeckle=ctk.CTkLabel(specklePanel, image=icon, text="   Ruido speckle", compound="left", font=("Roboto", 14, "bold"))
        labelSpeckle.pack(side="top", anchor="nw", padx=10, pady=5)
        labelSpeckle.image=icon

        #Entradas de texto
        panelBoxS=ctk.CTkFrame(specklePanel, fg_color="transparent", corner_radius=8, border_width=0)
        panelBoxS.pack(fill="x", padx=10, pady=10)
        self.muSpeckle=self.createNumberBox(panelBoxS, "Media (μ):", allowNegative=False)
        self.sigmaSpeckle=self.createNumberBox(panelBoxS, "Desviación (σ):", allowNegative=False)

        #Botón para ejecutar escala
        ctk.CTkButton(specklePanel, text="Agregar ruido speckle", command=self.applySpeckle,fg_color="#FFA600", hover_color="#CC8500", text_color="#FFFFFF"
        ).pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(self.scrollFrame, text="Tratado de ruido",font=("Roboto", 12, "bold")).pack(pady=(15, 0))

        ###Gaussian blur###
        blurPanel=ctk.CTkFrame(self.scrollFrame, corner_radius=15, border_width=1)
        blurPanel.pack(fill="x", padx=10, pady=10)

        icon=self.loadIcon("assets/images/blur.png", 40, 40) # Asegúrate de tener este icono
        labelBlur=ctk.CTkLabel(blurPanel, image=icon, text="   Filtro de gaussiano",compound="left", font=("Roboto", 14, "bold"))
        labelBlur.pack(side="top", anchor="nw", padx=10, pady=5)
        labelBlur.image = icon

        #Slider
        self.kernelLabel=ctk.CTkLabel(blurPanel, text="Tamaño del Kernel: 5x5")
        self.kernelLabel.pack(pady=(10, 0))

        self.sliderKernel=ctk.CTkSlider(blurPanel, from_=1, to=51, number_of_steps=25,command=lambda v: self.updateSliderFG(v))
        self.sliderKernel.set(5)
        self.sliderKernel.pack(fill="x", padx=20, pady=5)

        #NumberBox
        panelBoxB=ctk.CTkFrame(blurPanel, fg_color="transparent", corner_radius=8, border_width=0)
        panelBoxB.pack(fill="x", padx=10, pady=10)
        self.sigmaBlur = self.createNumberBox(panelBoxB, "Sigma (σ):", allowNegative=False)

        #Botón
        ctk.CTkButton(blurPanel, text="Aplicar filtro gaussiano",command=self.applyGaussianBlur, 
                    fg_color="#FFA600", hover_color="#CC8500", text_color="#FFFFFF").pack(fill="x", padx=20, pady=15)


    def updateSliderSP(self, value, slider):
        #Función que actualiza el slider de sal y pimienta
        salt=int(value)     #Obtenemos el valor de sal
        pepper=100-salt     #Calculamos el porcentaje de pimienta
        slider.configure(text="Sal: "+str(salt)+"% ---- Pimienta: "+str(pepper)+"%")    #Actualizamos slider


    def applyGauss(self):
        #Función para aplicar el ruido gaussiano
        image, name = self.getImage()   #Obtenemos la imagen
        if image is not None:
            try:
                mu=float(self.muGauss.get())        #Obtenemos mu
                sigma=float(self.sigmaGauss.get())  #Obtenemos sigma
                if sigma < 0:
                    messagebox.showwarning("Atención", "La desviación estandar no pueden ser menor a 0")
                    return
            except: #Si están mal enviamos advertencia
                messagebox.showerror("Error", "Valores inválidos en el ruido gaussiano")
                return
            result = self.noise.gaussiano(image, mu, sigma) #Aplicamos el ruido
            self.showResult(result, name, "ruido_gaussiano")    #Mostramos el resultado

    def applySaltAndPepper(self):
        #Función para aplicar el ruido sal y pimienta
        image, name = self.getImage()   #Obtenemos la imagen
        if image is not None:
            cantidad=self.sliderCantidad.get()/100  #Obtenemos la cantidad y dividimos a 100 para tener una probabilidad de tipo 0 a 1
            salt=self.sliderPorcentaje.get()/100    #Obtenemos el porcentaje de sal en tipo 0 a 1
            result = self.noise.saltAndPepper(image, cantidad, salt)#Aplicamos el ruido
            self.showResult(result, name, "ruido_salypimienta")#Mostramos el resultado

    def applySpeckle(self):
        #Función para aplicar el ruido speckle
        image, name = self.getImage()   #Obtenemos la imagen
        if image is not None:
            try:
                mu=float(self.muSpeckle.get())        #Obtenemos mu
                sigma=float(self.sigmaSpeckle.get())  #Obtenemos sigma
                if sigma<0:
                    messagebox.showwarning("Atención", "La desviación estandar no pueden ser menor a 0")
                    return
            except: #Si están mal enviamos advertencia
                messagebox.showerror("Error", "Valores inválidos en ruido speckle")
                return
            result = self.noise.speckle(image, mu, sigma) #Aplicamos el ruido
            self.showResult(result, name, "ruido_speckle")    #Mostramos el resultado
    
    def updateSliderFG(self, value):
        #Función para actualizar la etiqueta del slider filtro gaussiano
        k=int(value)
        if k%2==0:#Solo impares
            k+=1
        self.kernelLabel.configure(text="Tamaño del Kernel: "+str(k)+"x"+str(k))

    def applyGaussianBlur(self):
        #Función para aplicar el filtro gaussiano
        #obtener imagen actual
        image, name = self.getImage()
        if image is not None:
            kernel = int(self.sliderKernel.get())
            if kernel % 2 == 0:
                kernel += 1 # Asegurar que sea impar
            try:
                sigma=float(self.sigmaBlur.get())
                if sigma<0:
                    messagebox.showwarning("Atención", "La desviación estandar no pueden ser menor a 0")
                    return
            except: #Si están mal enviamos advertencia
                messagebox.showerror("Error", "Valores inválidos en ruido speckle")
                return

            result=self.noise.gaussianBlur(image, kernel, sigma)
            self.showResult(result, name, "filtro_gaussiano")
