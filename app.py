"""Visualab-Aplicación de procesamiento de imágenes
---------------------------------------------------
Autor: Jonathan Ivan Rojas Romero
Grupo:4BM1
Versión: 1.0
Fecha: Abril 3, 2026

Descripción:
Aplicación desarrollada con CustomTkinter para la visualización
y manipulación de imágenes, incluye: Generación del histograma,
transformaciones gemétricas, operaciones con escalar, operaciones
aritméticas y lógicas entre imágenes, manejo de mapas de color, ruido y
etiquetado de componentes."""

import customtkinter as ctk
from core.Interface import Interface
import os
import sys

def resourcePath(relativePath):
        #Función para cargar recursos
        try:
            basePath = sys._MEIPASS
        except Exception:
            basePath = os.path.abspath(".")
        return os.path.join(basePath, relativePath)

if __name__ == "__main__":
    #Desde aquí parte el programa

    #Definimos un tema para los colores y tipografías
    ctk.set_default_color_theme(resourcePath("assets/themes/themeDark.json"))

    #Creamos una interfaz con customtkinter
    root = ctk.CTk()
    app = Interface(root, "Visualab", resourcePath("assets/images/logoVisualab.ico"))
    root.mainloop()

