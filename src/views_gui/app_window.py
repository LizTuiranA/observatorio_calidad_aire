"""Contenedor principal GUI para navegar entre modulos del proyecto."""

import importlib
import tkinter as tk
from tkinter import messagebox, ttk

from src.views_gui.widgets_estado import EstadoWidget


class AppWindow:
    """Ventana principal con acceso a modulos de Alertas/Estaciones/Mediciones."""

    MODULOS = {
        "Alertas": ("src.views_gui.alertas_window", "AlertasWindow"),
        "Estaciones": ("src.views_gui.estaciones_window", "EstacionesWindow"),
        "Mediciones": ("src.views_gui.mediciones_window", "MedicionesWindow"),
    }

    def __init__(self, root: tk.Tk | tk.Toplevel) -> None:
        self.root = root
        self.root.title("Observatorio de Calidad del Aire")
        self._crear_layout()

    def _crear_layout(self) -> None:
        frame = ttk.Frame(self.root, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(frame, text="Menu principal", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )
        ttk.Label(
            frame,
            text="Seleccione un modulo para gestionar informacion del observatorio.",
        ).grid(row=1, column=0, sticky="w", pady=(0, 12))

        botonera = ttk.Frame(frame)
        botonera.grid(row=2, column=0, sticky="w")
        ttk.Button(botonera, text="Alertas", command=lambda: self.abrir_modulo("Alertas")).grid(
            row=0, column=0, padx=(0, 6)
        )
        ttk.Button(
            botonera,
            text="Estaciones",
            command=lambda: self.abrir_modulo("Estaciones"),
        ).grid(row=0, column=1, padx=(0, 6))
        ttk.Button(
            botonera,
            text="Mediciones",
            command=lambda: self.abrir_modulo("Mediciones"),
        ).grid(row=0, column=2)

        acciones = ttk.Frame(frame)
        acciones.grid(row=3, column=0, sticky="w", pady=(10, 0))
        ttk.Button(acciones, text="Salir", command=self.cerrar_aplicacion).grid(row=0, column=0)

        self.estado = EstadoWidget(frame)
        self.estado.mostrar("Listo. Seleccione un modulo.", "info")
        self.estado.label.grid(row=4, column=0, sticky="w", pady=(12, 0))

    def abrir_modulo(self, nombre_modulo: str) -> bool:
        """Abre una ventana hija del modulo solicitado."""
        self.estado.mostrar(f"Abriendo modulo {nombre_modulo}...", "info")
        modulo_info = self.MODULOS.get(nombre_modulo)
        if modulo_info is None:
            self.estado.mostrar(f"Error: modulo {nombre_modulo} no soportado", "error")
            return False

        path_modulo, nombre_clase = modulo_info
        try:
            modulo = importlib.import_module(path_modulo)
            clase_ventana = getattr(modulo, nombre_clase)
            child = tk.Toplevel(self.root)
            clase_ventana(child)
        except Exception as error:  # noqa: BLE001 - GUI debe capturar y notificar
            self.estado.mostrar(f"Error al abrir {nombre_modulo}: {error}", "error")
            return False

        self.estado.mostrar(f"Modulo {nombre_modulo} abierto correctamente", "success")
        return True

    def cerrar_aplicacion(self) -> bool:
        """Cierra la aplicacion con confirmacion del usuario."""
        confirmar = messagebox.askyesno("Confirmar salida", "Desea cerrar la aplicacion?")
        if not confirmar:
            self.estado.mostrar("Salida cancelada por el usuario", "info")
            return False
        self.root.destroy()
        return True


def ejecutar() -> None:
    root = tk.Tk()
    AppWindow(root)
    root.mainloop()


if __name__ == "__main__":
    ejecutar()
