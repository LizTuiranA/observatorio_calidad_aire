"""Pestana GUI para EstacionAmbiental."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from src.controllers.estacion_controller import EstacionController
from src.exceptions.custom_exceptions import RegistroNoEncontradoError
from src.models.estacion_ambiental import DuplicateEstacionError, EstacionValidationError
from src.views_gui_v2.widgets_estado import EstadoWidget


class EstacionesTab:
    """Pantalla de estaciones con listado y CRUD respetando MVC."""

    def __init__(self, parent: ttk.Frame, controller: EstacionController | None = None) -> None:
        self.parent = parent
        self.controller = controller or EstacionController()

        contenedor = ttk.Frame(parent, padding=8)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(1, weight=1)

        cabecera = ttk.Frame(contenedor)
        cabecera.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(
            cabecera,
            text="Modulo EstacionAmbiental",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            cabecera,
            text="Consulta, crea, actualiza y elimina estaciones usando EstacionController.",
            foreground="#4b5563",
        ).pack(anchor="w")

        cuerpo = ttk.Panedwindow(contenedor, orient="horizontal")
        cuerpo.grid(row=1, column=0, sticky="nsew")

        self._formulario = ttk.LabelFrame(cuerpo, text="Datos de la estacion", padding=12)
        self._listado = ttk.LabelFrame(cuerpo, text="Listado de estaciones", padding=12)
        cuerpo.add(self._formulario, weight=1)
        cuerpo.add(self._listado, weight=2)

        self._id = tk.StringVar()
        self._nombre = tk.StringVar()
        self._municipio = tk.StringVar()
        self._tipo = tk.StringVar()
        self._estado = tk.StringVar(value="Activa")
        self._busqueda = tk.StringVar()
        self._estado_widget: EstadoWidget | None = None

        self._crear_formulario()
        self._crear_listado()
        self.refrescar()

    def _crear_formulario(self) -> None:
        self._formulario.columnconfigure(1, weight=1)

        ttk.Label(self._formulario, text="ID estacion").grid(row=0, column=0, sticky="w", pady=4, padx=(0, 8))
        ttk.Entry(self._formulario, textvariable=self._id).grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Label(self._formulario, text="Nombre").grid(row=1, column=0, sticky="w", pady=4, padx=(0, 8))
        ttk.Entry(self._formulario, textvariable=self._nombre).grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(self._formulario, text="Municipio").grid(row=2, column=0, sticky="w", pady=4, padx=(0, 8))
        ttk.Entry(self._formulario, textvariable=self._municipio).grid(row=2, column=1, sticky="ew", pady=4)

        ttk.Label(self._formulario, text="Tipo estacion").grid(row=3, column=0, sticky="w", pady=4, padx=(0, 8))
        ttk.Entry(self._formulario, textvariable=self._tipo).grid(row=3, column=1, sticky="ew", pady=4)

        ttk.Label(self._formulario, text="Estado").grid(row=4, column=0, sticky="w", pady=4, padx=(0, 8))
        ttk.Combobox(
            self._formulario,
            textvariable=self._estado,
            values=("Activa", "Inactiva"),
            state="readonly",
        ).grid(row=4, column=1, sticky="ew", pady=4)

        acciones = ttk.Frame(self._formulario)
        acciones.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(12, 4))
        ttk.Button(acciones, text="Crear", command=self._crear).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Buscar", command=self._buscar).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Actualizar", command=self._actualizar).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Eliminar", command=self._eliminar).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Limpiar", command=self._limpiar).pack(side="left")

        busqueda = ttk.Frame(self._formulario)
        busqueda.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        ttk.Label(busqueda, text="Buscar por ID").pack(side="left", padx=(0, 8))
        ttk.Entry(busqueda, textvariable=self._busqueda, width=24).pack(side="left", fill="x", expand=True)
        ttk.Button(busqueda, text="Consultar", command=self._consultar_por_id).pack(side="left", padx=(8, 0))

        self._estado_widget = EstadoWidget(self._formulario)
        self._estado_widget.label.grid(row=7, column=0, columnspan=2, sticky="w", pady=(12, 0))

    def _crear_listado(self) -> None:
        toolbar = ttk.Frame(self._listado)
        toolbar.pack(fill="x", pady=(0, 8))
        ttk.Button(toolbar, text="Refrescar", command=self.refrescar).pack(side="left")

        columnas = ("id", "nombre", "municipio", "tipo", "estado")
        self._tabla = ttk.Treeview(self._listado, columns=columnas, show="headings", height=14)
        for columna, titulo in (
            ("id", "ID"),
            ("nombre", "Nombre"),
            ("municipio", "Municipio"),
            ("tipo", "Tipo"),
            ("estado", "Estado"),
        ):
            self._tabla.heading(columna, text=titulo)
            self._tabla.column(columna, width=120, anchor="w")

        self._tabla.pack(fill="both", expand=True, side="left")
        scroll = ttk.Scrollbar(self._listado, orient="vertical", command=self._tabla.yview)
        self._tabla.configure(yscrollcommand=scroll.set)
        scroll.pack(fill="y", side="right")
        self._tabla.bind("<<TreeviewSelect>>", self._cargar_seleccion)

    def refrescar(self) -> None:
        for item in self._tabla.get_children():
            self._tabla.delete(item)

        try:
            for estacion in self.controller.listar_estaciones():
                self._tabla.insert(
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
            self._estado_widget.mostrar("Listado actualizado", "info")
        except Exception as error:  # pragma: no cover
            self._estado_widget.mostrar(str(error), "error")

    def _crear(self) -> None:
        try:
            estacion = self.controller.crear_estacion(
                self._id.get(),
                self._nombre.get(),
                self._municipio.get(),
                self._tipo.get(),
                self._estado.get(),
            )
        except (EstacionValidationError, DuplicateEstacionError, RegistroNoEncontradoError) as error:
            self._estado_widget.mostrar(str(error), "error")
            return

        self._estado_widget.mostrar(f"Estacion creada: {estacion.id_estacion}", "success")
        self.refrescar()
        self._limpiar_formulario()

    def _buscar(self) -> None:
        id_estacion = self._id.get().strip() or self._busqueda.get().strip()
        if not id_estacion:
            self._estado_widget.mostrar("Ingrese un ID para buscar", "error")
            return

        try:
            estacion = self.controller.buscar_estacion(id_estacion)
        except Exception as error:
            self._estado_widget.mostrar(str(error), "error")
            return

        if estacion is None:
            self._estado_widget.mostrar("Estacion no encontrada", "error")
            return

        self._cargar_en_formulario(estacion.id_estacion, estacion.nombre, estacion.municipio, estacion.tipo_estacion, estacion.estado)
        self._estado_widget.mostrar(f"Estacion encontrada: {estacion.id_estacion}", "success")

    def _consultar_por_id(self) -> None:
        self._buscar()

    def _actualizar(self) -> None:
        try:
            estacion = self.controller.actualizar_estacion(
                self._id.get(),
                self._nombre.get(),
                self._municipio.get(),
                self._tipo.get(),
                self._estado.get(),
            )
        except (EstacionValidationError, DuplicateEstacionError, RegistroNoEncontradoError) as error:
            self._estado_widget.mostrar(str(error), "error")
            return

        self._estado_widget.mostrar(f"Estacion actualizada: {estacion.id_estacion}", "success")
        self.refrescar()

    def _eliminar(self) -> None:
        id_estacion = self._id.get().strip() or self._busqueda.get().strip()
        if not id_estacion:
            self._estado_widget.mostrar("Ingrese un ID para eliminar", "error")
            return

        if not messagebox.askyesno("Confirmar", f"Eliminar estacion '{id_estacion}'?"):
            return

        try:
            self.controller.eliminar_estacion(id_estacion)
        except (EstacionValidationError, DuplicateEstacionError, RegistroNoEncontradoError) as error:
            self._estado_widget.mostrar(str(error), "error")
            return

        self._estado_widget.mostrar(f"Estacion eliminada: {id_estacion}", "success")
        self._limpiar_formulario()
        self.refrescar()

    def _cargar_seleccion(self, _event: tk.Event) -> None:
        seleccion = self._tabla.selection()
        if not seleccion:
            return
        valores = self._tabla.item(seleccion[0], "values")
        if not valores:
            return
        self._cargar_en_formulario(*valores)

    def _cargar_en_formulario(self, id_estacion: str, nombre: str, municipio: str, tipo: str, estado: str) -> None:
        self._id.set(id_estacion)
        self._nombre.set(nombre)
        self._municipio.set(municipio)
        self._tipo.set(tipo)
        self._estado.set(estado)
        self._busqueda.set(id_estacion)

    def _limpiar(self) -> None:
        self._limpiar_formulario()
        self._estado_widget.mostrar("Formulario limpio", "info")

    def _limpiar_formulario(self) -> None:
        self._id.set("")
        self._nombre.set("")
        self._municipio.set("")
        self._tipo.set("")
        self._estado.set("Activa")
        self._busqueda.set("")
