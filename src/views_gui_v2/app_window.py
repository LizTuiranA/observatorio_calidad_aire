"""Ventana principal con navegacion por pestanas (ttk.Notebook)."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from src.views_gui_v2.alertas_tab import AlertasTab
from src.views_gui_v2.estaciones_tab import EstacionesTab
from src.views_gui_v2.mediciones_tab import MedicionesTab
from src.views_gui_v2.municipios_tab import MunicipiosTab
from src.services.session_context import SesionActiva


class AppWindow:
    """Ventana principal: un Notebook con un tab por modulo."""

    def __init__(self, root: tk.Tk, session: SesionActiva) -> None:
        self.root = root
        self.session = session
        self.can_write = session.puede_escribir
        self.root.title("Observatorio de Calidad del Aire")
        self.root.resizable(True, True)
        self._crear_layout()

    def _crear_layout(self) -> None:
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

        if not self.can_write:
            self._aplicar_solo_lectura(
                tab_estaciones, tab_municipios, tab_mediciones, tab_alertas
            )

    def _aplicar_solo_lectura(self, *contenedores: ttk.Frame) -> None:
        botones_bloqueados = {
            "anadir",
            "añadir",
            "crear",
            "actualizar",
            "eliminar",
            "guardar",
            "registrar",
        }
        for contenedor in contenedores:
            self._recorrer_widgets(contenedor, botones_bloqueados)

    def _recorrer_widgets(self, widget: tk.Misc, botones_bloqueados: set[str]) -> None:
        for hijo in widget.winfo_children():
            if isinstance(hijo, ttk.Button):
                texto = str(hijo.cget("text")).strip().lower()
                if texto in botones_bloqueados:
                    hijo.state(["disabled"])
            self._recorrer_widgets(hijo, botones_bloqueados)

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
