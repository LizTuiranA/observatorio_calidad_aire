"""Ventana principal con navegacion por pestanas (ttk.Notebook)."""

import tkinter as tk
from tkinter import messagebox, ttk

from src.views_gui_v2.alertas_tab import AlertasTab
from src.views_gui_v2.estaciones_tab import EstacionesTab
from src.views_gui_v2.mediciones_tab import MedicionesTab
from src.views_gui_v2.municipios_tab import MunicipiosTab


class AppWindow:
    """Ventana principal: un Notebook con un tab por modulo."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Observatorio de Calidad del Aire")
        self.root.resizable(True, True)
        self._crear_layout()

    def _crear_layout(self) -> None:
        barra = ttk.Frame(self.root)
        barra.pack(fill="x", padx=8, pady=(8, 0))
        ttk.Button(
            barra, text="Cerrar sesion", command=self._cerrar_sesion
        ).pack(side="right")

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        tab_estaciones = ttk.Frame(notebook)
        tab_municipios = ttk.Frame(notebook)
        tab_mediciones = ttk.Frame(notebook)
        tab_alertas = ttk.Frame(notebook)

        notebook.add(tab_estaciones, text="  Estaciones  ")
        notebook.add(tab_municipios, text="  Municipios  ")
        notebook.add(tab_mediciones, text="  Mediciones  ")
        notebook.add(tab_alertas, text="  Alertas  ")

        EstacionesTab(tab_estaciones)
        MunicipiosTab(tab_municipios)
        MedicionesTab(tab_mediciones)
        AlertasTab(tab_alertas)

    def _cerrar_sesion(self) -> None:
        if messagebox.askyesno("Cerrar sesion", "Desea cerrar la sesion y salir?"):
            self.root.destroy()


def ejecutar() -> None:
    root = tk.Tk()
    AppWindow(root)
    root.mainloop()


if __name__ == "__main__":
    ejecutar()
