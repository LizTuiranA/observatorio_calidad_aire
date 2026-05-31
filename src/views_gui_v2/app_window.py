"""Ventana principal con navegacion por pestanas (ttk.Notebook)."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from src.views_gui_v2.alertas_tab import AlertasTab
from src.views_gui_v2.estaciones_tab import EstacionesTab
from src.views_gui_v2.mediciones_tab import MedicionesTab
from src.views_gui_v2.municipios_tab import MunicipiosTab
from src.views_gui_v2.visitante_tab import VisitanteTab
from src.services.session_context import SesionActiva


class AppWindow:
    """Ventana principal: un Notebook con un tab por modulo o vista de solo lectura."""

    def __init__(self, root: tk.Tk, session: SesionActiva) -> None:
        self.root = root
        self.session = session
        self.can_write = session.puede_escribir
        self.root.title("Observatorio de Calidad del Aire")
        self.root.resizable(True, True)
        self._crear_layout()

    def _crear_layout(self) -> None:
        # --- Barra superior (Header) ---
        barra = ttk.Frame(self.root, padding=(8, 8, 8, 0))
        barra.pack(fill="x")

        titulo = ttk.Frame(barra)
        titulo.pack(side="left", fill="x", expand=True)
        ttk.Label(
            titulo,
            text="Observatorio de Calidad del Aire",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            titulo,
            text=f"Sesion activa: {self.session.usuario} | Rol: {self.session.rol}",
            foreground="#4b5563",
        ).pack(anchor="w")

        ttk.Button(barra, text="Cerrar sesion", command=self._cerrar_sesion).pack(
            side="right"
        )

        # --- Contenedor Principal ---
        main_container = ttk.Frame(self.root, padding=8)
        main_container.pack(fill="both", expand=True)

        # --- Lógica de separación de vistas ---
        if self.can_write:
            # SI ES EMPLEADO/ADMIN: Muestra las pestañas con CRUD completo
            notebook = ttk.Notebook(main_container)
            notebook.pack(fill="both", expand=True)

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
        else:
            # SI ES VISITANTE: Muestra la interfaz exclusiva de consulta
            VisitanteTab(main_container)

    def _cerrar_sesion(self) -> None:
        if messagebox.askyesno("Cerrar sesion", "Desea cerrar la sesion y salir?"):
            self.root.destroy()


def ejecutar(session: SesionActiva | None = None) -> None:
    if session is None:
        session = SesionActiva(usuario="empleado", rol="empleado")
    root = tk.Tk()
    AppWindow(root, session=session)
    root.mainloop()


if __name__ == "__main__":
    ejecutar()