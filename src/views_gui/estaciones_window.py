"""Ventana Tkinter para gestion de estaciones ambientales."""

import tkinter as tk
from tkinter import messagebox, ttk

from src.controllers.estacion_controller import EstacionController
from src.exceptions.custom_exceptions import RegistroNoEncontradoError
from src.models.estacion_ambiental import DuplicateEstacionError, EstacionValidationError
from src.views_gui.widgets_estado import EstadoWidget


def validar_campos_obligatorios(campos: dict[str, str]) -> tuple[bool, str]:
    """Valida campos obligatorios del formulario."""
    for nombre, valor in campos.items():
        if not str(valor).strip():
            return False, f"El campo '{nombre}' es obligatorio"
    return True, ""


class EstacionesWindow:
    """Formulario GUI para crear y actualizar estaciones."""

    TIPOS = ("Fija", "Movil")
    ESTADOS = ("Activa", "Inactiva")

    def __init__(self, root: tk.Tk | tk.Toplevel, controller: EstacionController | None = None) -> None:
        self.root = root
        self.controller = controller or EstacionController()
        self.root.title("Gestion de Estaciones")
        self._crear_variables()
        self._crear_layout()
        self.refrescar_lista()

    def _crear_variables(self) -> None:
        self.id_estacion_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.municipio_var = tk.StringVar()
        self.tipo_var = tk.StringVar(value=self.TIPOS[0])
        self.estado_var = tk.StringVar(value=self.ESTADOS[0])

    def _crear_layout(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        campos = [
            ("ID estacion", self.id_estacion_var),
            ("Nombre", self.nombre_var),
            ("Municipio", self.municipio_var),
        ]
        for idx, (texto, variable) in enumerate(campos):
            ttk.Label(frame, text=texto).grid(row=idx, column=0, sticky="w", padx=(0, 8), pady=4)
            ttk.Entry(frame, textvariable=variable, width=34).grid(row=idx, column=1, sticky="ew", pady=4)

        ttk.Label(frame, text="Tipo").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Combobox(frame, textvariable=self.tipo_var, values=self.TIPOS, state="readonly").grid(
            row=3, column=1, sticky="ew", pady=4
        )

        ttk.Label(frame, text="Estado").grid(row=4, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Combobox(frame, textvariable=self.estado_var, values=self.ESTADOS, state="readonly").grid(
            row=4, column=1, sticky="ew", pady=4
        )

        botonera = ttk.Frame(frame)
        botonera.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10, 6))
        ttk.Button(botonera, text="Crear estacion", command=self.crear_estacion).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(botonera, text="Actualizar estacion", command=self.actualizar_estacion).grid(row=0, column=1, padx=(0, 6))
        ttk.Button(botonera, text="Limpiar", command=self.limpiar_formulario).grid(row=0, column=2, padx=(0, 6))
        ttk.Button(botonera, text="Cancelar", command=self.cancelar).grid(row=0, column=3)

        self.tabla = ttk.Treeview(
            frame,
            columns=("id", "nombre", "municipio", "tipo", "estado"),
            show="headings",
            height=8,
        )
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("municipio", text="Municipio")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.heading("estado", text="Estado")
        self.tabla.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=(4, 0))

        self.estado = EstadoWidget(frame)
        self.estado.label.grid(row=7, column=0, columnspan=2, sticky="w", pady=(8, 0))

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(6, weight=1)

    def _datos_formulario(self) -> dict[str, str]:
        return {
            "id_estacion": self.id_estacion_var.get(),
            "nombre": self.nombre_var.get(),
            "municipio": self.municipio_var.get(),
            "tipo_estacion": self.tipo_var.get(),
            "estado": self.estado_var.get(),
        }

    def crear_estacion(self) -> bool:
        self.estado.mostrar("Guardando estacion...", "info")
        datos = self._datos_formulario()
        valido, mensaje = validar_campos_obligatorios(
            {
                "id_estacion": datos["id_estacion"],
                "nombre": datos["nombre"],
                "municipio": datos["municipio"],
            }
        )
        if not valido:
            self.estado.mostrar(mensaje, "error")
            return False

        try:
            self.controller.crear_estacion(**datos)
        except (DuplicateEstacionError, EstacionValidationError, ValueError) as error:
            self.estado.mostrar(f"Error: {error}", "error")
            return False

        self.refrescar_lista()
        self.estado.mostrar("Estacion creada correctamente", "success")
        return True

    def actualizar_estacion(self) -> bool:
        datos = self._datos_formulario()
        valido, mensaje = validar_campos_obligatorios(
            {
                "id_estacion": datos["id_estacion"],
                "nombre": datos["nombre"],
                "municipio": datos["municipio"],
            }
        )
        if not valido:
            self.estado.mostrar(mensaje, "error")
            return False

        confirmar = messagebox.askyesno("Confirmar", "Desea actualizar la estacion seleccionada?")
        if not confirmar:
            self.estado.mostrar("Actualizacion cancelada por usuario", "info")
            return False

        self.estado.mostrar("Actualizando estacion...", "info")
        try:
            self.controller.actualizar_estacion(**datos)
        except (EstacionValidationError, RegistroNoEncontradoError, ValueError) as error:
            self.estado.mostrar(f"Error: {error}", "error")
            return False

        self.refrescar_lista()
        self.estado.mostrar("Estacion actualizada correctamente", "success")
        return True

    def refrescar_lista(self) -> None:
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for estacion in self.controller.listar_estaciones():
            self.tabla.insert(
                "",
                "end",
                values=(
                    estacion.id_estacion,
                    estacion.nombre,
                    estacion.municipio,
                    estacion.tipo_estacion,
                    estacion.estado,
                ),
            )

    def limpiar_formulario(self) -> None:
        self.id_estacion_var.set("")
        self.nombre_var.set("")
        self.municipio_var.set("")
        self.tipo_var.set(self.TIPOS[0])
        self.estado_var.set(self.ESTADOS[0])
        self.estado.mostrar("Formulario limpio", "info")

    def cancelar(self) -> None:
        self.limpiar_formulario()
        self.estado.mostrar("Operacion cancelada", "info")


def ejecutar() -> None:
    root = tk.Tk()
    EstacionesWindow(root)
    root.mainloop()


if __name__ == "__main__":
    ejecutar()
