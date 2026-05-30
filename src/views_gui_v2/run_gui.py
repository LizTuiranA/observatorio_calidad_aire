"""Punto de entrada para ejecutar la interfaz grafica con Notebook."""

from dotenv import load_dotenv

from src.views_gui_v2.app_window import ejecutar


if __name__ == "__main__":
    load_dotenv()
    ejecutar()
