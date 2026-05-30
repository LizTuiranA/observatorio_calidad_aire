"""Tab de alertas con flujo minimo para crear, registrar y reportar."""

from __future__ import annotations

from datetime import datetime
from pprint import pformat
import tkinter as tk
from tkinter import messagebox, ttk

from src.controllers.alerta_controller import AlertaController
from src.views_gui_v2.widgets_estado import EstadoWidget


class AlertasTab:
    """Pestana de alertas conectada al controlador real."""

    def __init__(self, parent: ttk.Frame, controller: AlertaController | None = None) -> None:
        self.controller = controller or AlertaController()
        self._alerta_seleccionada_id: str | None = None
        self._ultima_alerta = None

        contenedor = ttk.Frame(parent)
        contenedor.pack(fill="both", expand=True, padx=6, pady=6)
        contenedor.columnconfigure(0, weight=1)
        contenedor.columnconfigure(1, weight=1)
        contenedor.rowconfigure(1, weight=1)

        self._construir_formulario(contenedor)
        self._construir_listado(contenedor)
        self._construir_reporte(contenedor)
        self.refrescar()

    def _construir_formulario(self, parent: ttk.Frame) -> None:
        marco = ttk.LabelFrame(parent, text="Registrar alerta", padding=10)
        marco.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        marco.columnconfigure(1, weight=1)
        marco.columnconfigure(3, weight=1)

        self.id_alerta_var = tk.StringVar()
        self.id_medicion_var = tk.StringVar()
        self.municipio_var = tk.StringVar()
        self.valor_pm25_var = tk.StringVar()
        self.descripcion_var = tk.StringVar()
        self.fecha_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.nivel_var = tk.StringVar(value="Medio")
        self.estado_var = tk.StringVar(value="Activa")

        self._agregar_campo(marco, "ID alerta", self.id_alerta_var, 0, 0)
        self._agregar_campo(marco, "ID medicion", self.id_medicion_var, 0, 2)
        self._agregar_campo(marco, "Municipio", self.municipio_var, 1, 0)
        self._agregar_campo(marco, "Valor PM2.5", self.valor_pm25_var, 1, 2)
        self._agregar_campo(marco, "Descripcion", self.descripcion_var, 2, 0, colspan=3)
        self._agregar_campo(marco, "Fecha (YYYY-MM-DD)", self.fecha_var, 3, 0)

        ttk.Label(marco, text="Nivel manual").grid(row=3, column=2, sticky="w", padx=(12, 8), pady=4)
        ttk.Combobox(
            marco,
            textvariable=self.nivel_var,
            values=("Bajo", "Medio", "Alto"),
            state="readonly",
            width=20,
        ).grid(row=3, column=3, sticky="ew", pady=4)

        ttk.Label(marco, text="Estado").grid(row=4, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Combobox(
            marco,
            textvariable=self.estado_var,
            values=("Activa", "Cerrada"),
            state="readonly",
            width=20,
        ).grid(row=4, column=1, sticky="w", pady=4)

        acciones = ttk.Frame(marco)
        acciones.grid(row=5, column=0, columnspan=4, sticky="w", pady=(10, 0))
        ttk.Button(acciones, text="Crear manual", command=self._crear_manual).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Registrar critica", command=self._registrar_critica).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Generar reporte", command=self._generar_reporte).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Limpiar", command=self._limpiar).pack(side="left")

        self._estado = EstadoWidget(marco)
        self._estado.label.grid(row=6, column=0, columnspan=4, sticky="w", pady=(8, 0))

    def _agregar_campo(
        self,
        parent: ttk.LabelFrame,
        etiqueta: str,
        variable: tk.StringVar,
        fila: int,
        columna: int,
        colspan: int = 1,
    ) -> None:
        ttk.Label(parent, text=etiqueta).grid(row=fila, column=columna, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(parent, textvariable=variable).grid(
            row=fila,
            column=columna + 1,
            columnspan=colspan,
            sticky="ew",
            pady=4,
        )

    def _construir_listado(self, parent: ttk.Frame) -> None:
        marco = ttk.LabelFrame(parent, text="Alertas registradas", padding=10)
        marco.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        marco.columnconfigure(0, weight=1)
        marco.rowconfigure(1, weight=1)

        ttk.Button(marco, text="Refrescar", command=self.refrescar).grid(row=0, column=0, sticky="w", pady=(0, 6))

        columnas = ("id", "medicion", "nivel", "fecha", "estado")
        self._tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=8)
        for columna, titulo in zip(columnas, ("ID", "Medicion", "Nivel", "Fecha", "Estado")):
            self._tabla.heading(columna, text=titulo)
            self._tabla.column(columna, width=110, anchor="w")
        self._tabla.grid(row=1, column=0, sticky="nsew")
        self._tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)

        scroll = ttk.Scrollbar(marco, orient="vertical", command=self._tabla.yview)
        self._tabla.configure(yscrollcommand=scroll.set)
        scroll.grid(row=1, column=1, sticky="ns")

    def _construir_reporte(self, parent: ttk.Frame) -> None:
        marco = ttk.LabelFrame(parent, text="Reporte de alerta", padding=10)
        marco.grid(row=1, column=1, sticky="nsew")
        marco.columnconfigure(0, weight=1)
        marco.rowconfigure(0, weight=1)

        self._reporte = tk.Text(marco, height=16, wrap="word")
        self._reporte.grid(row=0, column=0, sticky="nsew")
        self._reporte.insert("end", "Selecciona una alerta o registra una nueva para ver su reporte.")
        self._reporte.configure(state="disabled")

    def _crear_manual(self) -> None:
        nivel = self.nivel_var.get().strip()
        try:
            alerta = self.controller.crear_alerta(
                id_alerta=self.id_alerta_var.get().strip(),
                id_medicion=self.id_medicion_var.get().strip(),
                nivel=nivel,
                descripcion=self.descripcion_var.get().strip(),
                fecha=self.fecha_var.get().strip(),
                estado=self.estado_var.get().strip(),
            )
        except Exception as error:  # pragma: no cover - la validacion real ya vive en el modelo/controlador
            self._estado.mostrar(str(error), "error")
            return

        self._ultima_alerta = alerta
        self._estado.mostrar(f"Alerta {alerta.id_alerta} guardada correctamente", "success")
        self.refrescar()
        self._mostrar_reporte(alerta)

    def _registrar_critica(self) -> None:
        try:
            valor = float(self.valor_pm25_var.get())
        except ValueError:
            self._estado.mostrar("Valor PM2.5 invalido", "error")
            return

        try:
            alerta = self.controller.registrar_alerta_critica(
                id_alerta=self.id_alerta_var.get().strip(),
                id_medicion=self.id_medicion_var.get().strip(),
                valor_pm25=valor,
                descripcion=self.descripcion_var.get().strip(),
                fecha=self.fecha_var.get().strip(),
                estado_inicial=self.estado_var.get().strip() or "Activa",
            )
        except Exception as error:  # pragma: no cover
            self._estado.mostrar(str(error), "error")
            return

        self._ultima_alerta = alerta
        self._estado.mostrar(
            f"Alerta critica {alerta.id_alerta} registrada con nivel {alerta.nivel}",
            "success",
        )
        self.refrescar()
        self._mostrar_reporte(alerta, valor_pm25=valor)

    def _generar_reporte(self) -> None:
        alerta = self._alerta_desde_seleccion() or self._ultima_alerta
        if alerta is None:
            self._estado.mostrar("Selecciona una alerta para generar el reporte", "error")
            return
        valor_pm25 = None
        try:
            valor_pm25 = float(self.valor_pm25_var.get())
        except ValueError:
            valor_pm25 = None
        self._mostrar_reporte(alerta, valor_pm25=valor_pm25)

    def _mostrar_reporte(self, alerta, valor_pm25: float | None = None) -> None:
        mediciones = []
        if valor_pm25 is not None:
            mediciones.append({"pm25": valor_pm25})
        reporte = self.controller.generar_reporte_alerta(
            alerta,
            municipio=self.municipio_var.get().strip(),
            mediciones=mediciones,
            recomendaciones=["Verificar fuentes de emision"] if alerta.nivel == "Alto" else [],
        )
        contenido = pformat(reporte.__dict__, sort_dicts=False)
        self._reporte.configure(state="normal")
        self._reporte.delete("1.0", "end")
        self._reporte.insert("end", contenido)
        self._reporte.configure(state="disabled")

    def _limpiar(self) -> None:
        for variable in (
            self.id_alerta_var,
            self.id_medicion_var,
            self.municipio_var,
            self.valor_pm25_var,
            self.descripcion_var,
        ):
            variable.set("")
        self.fecha_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.nivel_var.set("Medio")
        self.estado_var.set("Activa")
        self._alerta_seleccionada_id = None
        self._ultima_alerta = None
        self._estado.mostrar("Formulario limpiado", "info")

    def refrescar(self) -> None:
        for item in self._tabla.get_children():
            self._tabla.delete(item)
        try:
            for alerta in self.controller.listar_alertas():
                self._tabla.insert(
                    "",
                    "end",
                    values=(
                        alerta.id_alerta,
                        alerta.id_medicion,
                        alerta.nivel,
                        alerta.fecha,
                        alerta.estado,
                    ),
                )
        except Exception as error:  # pragma: no cover
            messagebox.showerror("Error al listar alertas", str(error))

    def _al_seleccionar(self, _event=None) -> None:
        seleccion = self._tabla.selection()
        if not seleccion:
            return
        valores = self._tabla.item(seleccion[0], "values")
        if not valores:
            return
        self._alerta_seleccionada_id = str(valores[0])
        alerta = self.controller.buscar_alerta(self._alerta_seleccionada_id)
        if alerta is not None:
            self._ultima_alerta = alerta
            self.id_alerta_var.set(alerta.id_alerta)
            self.id_medicion_var.set(alerta.id_medicion)
            self.descripcion_var.set(alerta.descripcion)
            self.fecha_var.set(alerta.fecha)
            self.nivel_var.set(alerta.nivel)
            self.estado_var.set(alerta.estado)
            self._estado.mostrar(f"Alerta {alerta.id_alerta} seleccionada", "info")

    def _alerta_desde_seleccion(self):
        if self._alerta_seleccionada_id is None:
            return None
        return self.controller.buscar_alerta(self._alerta_seleccionada_id)
