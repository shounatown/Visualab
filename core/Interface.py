import customtkinter as ctk
from .ButtonsFunctionalities import ButtonsFunctionalities
from .ColorMapControls import ColorMapControls
from .HistogramControls import HistogramControls
from .GeometricTransformationsControls import GeometricTransformationsControls
from .BasicOperationsControls import BasicOperationsControls
from .ImageOperationsControls import ImageOperationsControls
from .NoiseControls import NoiseControls
from .ConnectivityControls import ConnectivityControls
from .RegionSegmentationControls import RegionSegmentationControls


class Interface:
    #Interface está encargada de construir y organizar toda la interfaz gráfica

    def __init__(self, root, name, icon):
        #Constructor de la clase
        self.root = root
        self.root.title(name)
        root.iconbitmap(icon)

        #Configuración de pantalla
        #Maximiza la ventana
        self.root.after(0, lambda: self.root.state('zoomed'))

        #Ancho del menú lateral (1/6 de la pantalla)
        screenWidth = self.root.winfo_screenwidth()
        self.menuWidth = screenWidth // 5.5

        #Diccionario para las imágenes abiertas
        self.openedImages = {}
        #Set para evitar duplicados
        self.createdTabs = set()

        #Pestañas del menu
        self.options = ["Histograma",
                        "Transformaciones geométricas",
                        "Operaciones básicas",
                        "Operaciones entre imágenes",
                        "Mapas de color",
                        "Ruido",
                        "Etiquetado de componentes",
                        "Segmentación de una región"]


        self.setUpFrames()      #Crea los contenedores principales
        self.setUpPanel()       #Configura el panel

        #Clase que maneja la lógica de los botones
        self.bf = ButtonsFunctionalities(self.tabView, self.openedImages, self.createdTabs)
        self.setUpButtons()     #Crea los botones
        self.setUpMenu()        #Configura el menú

    def setUpFrames(self):
        #Esta función configura los frames
        #Frame izquierdo
        self.frameLeft = ctk.CTkFrame(self.root, width=self.menuWidth, corner_radius=0)
        self.frameLeft.pack(side="left", fill="y", padx=(10, 0), pady=10)
        self.frameLeft.pack_propagate(False)

        #Frame derecho
        self.frameRight = ctk.CTkFrame(self.root)
        self.frameRight.pack(side="right", fill="both", expand=True, padx=10, pady=10)


    def setUpButtons(self):
        #Está función inicia los botones principales para la carga y el guardado de imágenes

        ctk.CTkLabel(self.frameLeft, text="Archivos", font=("Roboto", 12, "bold")).pack(pady=(10, 5))

        #Botón para abrir imágenes
        self.bf.createIconButton("Cargar imagen", "assets/images/open.png", self.bf.openImage,"#78CD6C", "#77A971", self.frameLeft)

        #Botón para guardar imágenes
        self.bf.createIconButton("Guardar imagen", "assets/images/save.png", self.bf.saveImage,"#99B4D5", "#7789A5", self.frameLeft)

        #Botón para cerrar imágenes
        self.bf.createIconButton("Cerrar la pestaña actual", "assets/images/close.png", self.bf.closeImage,"#DD0808","#C00808", self.frameLeft)

        #Linea para separar
        ctk.CTkFrame(self.frameLeft, height=2, fg_color="#000000").pack(fill="x", padx=10, pady=15)

    def setUpMenu(self):
        #Esta función inicia el menu

        #Menú despegable
        self.menu = ctk.CTkOptionMenu(self.frameLeft, values=self.options, command=self.changeControls)
        self.menu.pack(fill="x", padx=15, pady=5)

        #Cambiar los controles de cada sección
        self.controls = ctk.CTkFrame(self.frameLeft, fg_color="transparent")
        self.controls.pack(fill="both", expand=True, padx=5, pady=10)
        self.changeControls("Histograma")   #"Histograma" por default

    def setUpPanel(self):
        #Esta función se encarga de mostrar el panel para las imágenes

        self.tabView = ctk.CTkTabview(self.frameRight)
        self.tabView.pack(fill="both", expand=True, padx=5, pady=5)

        #Definimos un tab de inicio
        self.tabView.add("Inicio")
        ctk.CTkLabel(self.tabView.tab("Inicio"), text="Bienvenido a Visualab\nCarga una imagen para empezar").pack(expand=True)

    def changeControls(self, seleccion):
        #Esta función se encarga de la lógica detrás del cambio de sección del menú

        #Limpiar el panel
        for widget in self.controls.winfo_children():
            widget.destroy()

        #Sección "Histograma"
        if seleccion=="Histograma":
            #Generamos los botones
            HistogramControls(self.controls, self.tabView, self.openedImages,self.createdTabs)

        #Sección "Trasformaciones geométricas"
        if seleccion=="Transformaciones geométricas":
            #Generamos los botones
            GeometricTransformationsControls(self.controls, self.tabView, self.openedImages,self.createdTabs)

        #Sección "Operaciones básicas"
        if seleccion=="Operaciones básicas":
            #Generamos los botones
            BasicOperationsControls(self.controls, self.tabView, self.openedImages,self.createdTabs)

        #Sección "Mapas de color"
        if seleccion=="Mapas de color":
            #Generamos los botones
            ColorMapControls(self.controls, self.tabView, self.openedImages,self.createdTabs)
            #Sección "Mapas de color"

        #Sección "Operaciones entre imágenes"
        if seleccion=="Operaciones entre imágenes":
            #Generamos los botones
            ImageOperationsControls(self.controls, self.tabView, self.openedImages,self.createdTabs)

        #Sección "Noise"
        if seleccion=="Ruido":
            #Generamos los botones
            NoiseControls(self.controls, self.tabView, self.openedImages,self.createdTabs)

        #Sección "Etiquetado de componentes"
        if seleccion=="Etiquetado de componentes":
            #Generamos los botones
            ConnectivityControls(self.controls, self.tabView, self.openedImages,self.createdTabs)

        #Sección "Segmentación de una región"
        if seleccion=="Segmentación de una región":
            #Generamos los botones
            RegionSegmentationControls(self.controls, self.tabView, self.openedImages,self.createdTabs)


