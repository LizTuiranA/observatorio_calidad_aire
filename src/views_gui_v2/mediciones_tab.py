"""Tab de Mediciones: sub-tabs (Anadir, Consultar, Actualizar, Eliminar) + listado fijo abajo."""

from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

from src.controllers.estacion_controller import EstacionController
from src.controllers.medicion_calidad_aire_controller import MedicionController
from src.controllers.municipio_controller import MunicipioController
from src.factories.medicion_factory import MedicionFactory
from src.models.medicion_calidad_aire import MedicionCalidadAirePM
from src.views_gui_v2.widgets_estado import EstadoWidget


class _ViewAdapter:
    """Adapta el contrato view del controller al EstadoWidget activo del tab."""

    def __init__(self) -> None:
        self._activo: EstadoWidget | None = None
        self.exito = False

    def usar(self, widget: EstadoWidget) -> None:
        self._activo = widget
        self.exito = False

    def show_message(self, msg: str) -> None:
        self.exito = True
        if self._activo is not None:
            self._activo.mostrar(msg, "success")

    def show_error(self, msg: str) -> None:
        self.exito = False
        if self._activo is not None:
            self._activo.mostrar(msg, "error")

    def show_mediciones(self, mediciones) -> None:  # noqa: D401
        pass


COLS = ("id", "estacion", "fecha", "valor", "nivel", "origen")
HEADS = ("ID", "Estacion", "Fecha", "Valor", "Nivel ICA", "Origen")

# Campos extra por tipo: {tipo: [(label, kwarg_name, opciones)]}.
# Para agregar un tipo nuevo, registralo en MedicionFactory y aniade su entrada aqui.
CAMPOS_POR_TIPO: dict[str, list[tuple[str, str, tuple]]] = {
    "PM": [("Diametro", "diametro_aerodinamico",
            (MedicionCalidadAirePM.PM25, MedicionCalidadAirePM.PM10))],
}


def _row(m) -> tuple:
    return (m.id, m.id_estacion, m.fecha.date().isoformat(), m.medicion, m.nivel, m.origen)


class MedicionesTab:
    """Pestana principal de mediciones de calidad del aire."""

    def __init__(
        self,
        parent: ttk.Frame,
        controller: MedicionController | None = None,
        estacion_controller: EstacionController | None = None,
        municipio_controller: MunicipioController | None = None,
    ) -> None:
        self.estacion_controller = estacion_controller or EstacionController()
        self.municipio_controller = municipio_controller or MunicipioController()
        self._view = _ViewAdapter()
        self.controller = controller or MedicionController(
            view=self._view,
            estacion_repository=self.estacion_controller.repository,
            municipio_repository=self.municipio_controller.repository,
        )
        self.controller.view = self._view

        contenedor = ttk.Frame(parent)
        contenedor.pack(fill="both", expand=True, padx=4, pady=4)

        nb = ttk.Notebook(contenedor)
        nb.pack(fill="both", expand=True)
        self._tab_anadir(nb)
        self._tab_consultar(nb)
        self._tab_actualizar(nb)
        self._tab_eliminar(nb)

        self._construir_listado(parent)
        self.refrescar()

    # ─── Listado inferior ───────────────────────────────────────────
    def _construir_listado(self, parent: ttk.Frame) -> None:
        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=4, pady=(4, 0))
        marco = ttk.LabelFrame(parent, text="Listado actual de mediciones", padding=6)
        marco.pack(fill="both", expand=False, padx=4, pady=4)
        marco.columnconfigure(0, weight=1)

        toolbar = ttk.Frame(marco)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        ttk.Button(toolbar, text="Refrescar", command=self.refrescar).pack(side="left")

        self._tabla = ttk.Treeview(marco, columns=COLS, show="headings", height=7)
        for c, h in zip(COLS, HEADS):
            self._tabla.heading(c, text=h)
            self._tabla.column(c, width=110, anchor="w")
        self._tabla.grid(row=1, column=0, sticky="nsew")
        sb = ttk.Scrollbar(marco, orient="vertical", command=self._tabla.yview)
        self._tabla.configure(yscrollcommand=sb.set)
        sb.grid(row=1, column=1, sticky="ns")

    def refrescar(self) -> None:
        for item in self._tabla.get_children():
            self._tabla.delete(item)
        try:
            for m in self.controller.obtener_mediciones():
                self._tabla.insert("", "end", values=_row(m))
        except Exception as e:  # pragma: no cover
            messagebox.showerror("Error al listar", str(e))

    # ─── Anadir ─────────────────────────────────────────────────────
    def _tab_anadir(self, nb: ttk.Notebook) -> None:
        frame = ttk.Frame(nb, padding=12)
        nb.add(frame, text="  Anadir medicion  ")

        tipos = MedicionFactory.tipos_disponibles()
        self._tipo_a = tk.StringVar(value=tipos[0] if tipos else "")
        self._id_a = tk.StringVar()
        self._dane_a = tk.StringVar()
        self._est_a = tk.StringVar()
        self._fecha_a = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self._valor_a = tk.StringVar()
        self._clasif_a = tk.StringVar(value="Nivel ICA: —")
        self._extras_a: dict[str, tk.StringVar] = {}

        ttk.Label(frame, text="Tipo medicion").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        cb_tipo = ttk.Combobox(frame, textvariable=self._tipo_a, values=tipos,
                               state="readonly", width=32)
        cb_tipo.grid(row=0, column=1, sticky="ew", pady=4)
        cb_tipo.bind("<<ComboboxSelected>>", lambda _e: self._render_extras_a())

        ttk.Label(frame, text="ID medicion").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(frame, textvariable=self._id_a, width=34).grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(frame, text="Codigo DANE municipio").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=4)
        self._cb_dane = ttk.Combobox(frame, textvariable=self._dane_a, width=32,
                                     postcommand=lambda: self._cargar_municipios(self._cb_dane))
        self._cb_dane.grid(row=2, column=1, sticky="ew", pady=4)

        ttk.Label(frame, text="ID estacion").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=4)
        self._cb_est_a = ttk.Combobox(frame, textvariable=self._est_a, width=32,
                                      postcommand=lambda: self._cargar_estaciones(self._cb_est_a))
        self._cb_est_a.grid(row=3, column=1, sticky="ew", pady=4)

        ttk.Label(frame, text="Fecha (YYYY-MM-DD)").grid(row=4, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(frame, textvariable=self._fecha_a, width=34).grid(row=4, column=1, sticky="ew", pady=4)

        ttk.Label(frame, text="Valor medicion").grid(row=5, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(frame, textvariable=self._valor_a, width=34).grid(row=5, column=1, sticky="ew", pady=4)

        self._extras_frame_a = ttk.Frame(frame)
        self._extras_frame_a.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 4))
        self._extras_frame_a.columnconfigure(1, weight=1)
        self._render_extras_a()

        bts = ttk.Frame(frame)
        bts.grid(row=7, column=0, columnspan=2, sticky="w", pady=(10, 4))
        ttk.Button(bts, text="Anadir", command=self._anadir).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(bts, text="Limpiar", command=self._limpiar_anadir).grid(row=0, column=1)

        ttk.Label(frame, textvariable=self._clasif_a).grid(row=8, column=0, columnspan=2, sticky="w", pady=(4, 0))
        self._estado_w_a = EstadoWidget(frame)
        self._estado_w_a.label.grid(row=9, column=0, columnspan=2, sticky="w", pady=(8, 0))
        frame.columnconfigure(1, weight=1)

    def _render_extras_a(self) -> None:
        for child in self._extras_frame_a.winfo_children():
            child.destroy()
        self._extras_a.clear()
        for i, (label, kwarg, opciones) in enumerate(
            CAMPOS_POR_TIPO.get(self._tipo_a.get(), [])
        ):
            var = tk.StringVar(value=opciones[0])
            self._extras_a[kwarg] = var
            ttk.Label(self._extras_frame_a, text=label).grid(
                row=i, column=0, sticky="w", padx=(0, 8), pady=4
            )
            ttk.Combobox(self._extras_frame_a, textvariable=var, values=opciones,
                         state="readonly").grid(row=i, column=1, sticky="ew", pady=4)

    def _anadir(self) -> None:
        for nombre, valor in {
            "tipo": self._tipo_a.get(),
            "id": self._id_a.get(),
            "codigo_dane": self._dane_a.get(),
            "id_estacion": self._est_a.get(),
            "fecha": self._fecha_a.get(),
            "valor": self._valor_a.get(),
        }.items():
            if not str(valor).strip():
                self._estado_w_a.mostrar(f"El campo '{nombre}' es obligatorio", "error")
                return

        try:
            valor = float(self._valor_a.get())
            if valor <= 0 or valor > 1000:
                raise ValueError
        except ValueError:
            self._estado_w_a.mostrar("Valor debe ser numerico entre 0 y 1000", "error")
            return

        try:
            fecha = datetime.fromisoformat(self._fecha_a.get().strip())
        except ValueError:
            self._estado_w_a.mostrar("Fecha invalida, use YYYY-MM-DD", "error")
            return

        extras = {k: v.get() for k, v in self._extras_a.items()}
        self._view.usar(self._estado_w_a)
        medicion = self.controller.crear_medicion(
            self._tipo_a.get(),
            id=self._id_a.get().strip().upper(),
            codigo_dane_municipio=self._dane_a.get().strip().upper(),
            id_estacion=self._est_a.get().strip().upper(),
            fecha=fecha,
            medicion=valor,
            **extras,
        )
        if medicion is None:
            return

        self._clasif_a.set(f"Nivel ICA: {medicion.nivel}")
        self.refrescar()

    def _limpiar_anadir(self) -> None:
        self._id_a.set("")
        self._dane_a.set("")
        self._est_a.set("")
        self._fecha_a.set(datetime.now().strftime("%Y-%m-%d"))
        self._valor_a.set("")
        self._clasif_a.set("Nivel ICA: —")
        self._render_extras_a()
        self._estado_w_a.mostrar("Formulario limpio", "info")

    # ─── Consultar ──────────────────────────────────────────────────
    def _tab_consultar(self, nb: ttk.Notebook) -> None:
        frame = ttk.Frame(nb, padding=12)
        nb.add(frame, text="  Consultar medicion  ")

        self._id_c = tk.StringVar()
        ttk.Label(frame, text="ID medicion").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        self._cb_consultar = ttk.Combobox(frame, textvariable=self._id_c, width=30,
                                          postcommand=lambda: self._cargar_ids_medicion(self._cb_consultar))
        self._cb_consultar.grid(row=0, column=1, sticky="ew", pady=4)
        ttk.Button(frame, text="Consultar", command=self._consultar).grid(row=0, column=2, padx=(8, 0))

        self._res_c = tk.StringVar(value="—")
        ttk.Label(frame, textvariable=self._res_c, wraplength=560, justify="left").grid(
            row=1, column=0, columnspan=3, sticky="w", pady=(12, 0)
        )
        self._estado_w_c = EstadoWidget(frame)
        self._estado_w_c.label.grid(row=2, column=0, columnspan=3, sticky="w", pady=(8, 0))
        frame.columnconfigure(1, weight=1)

    def _consultar(self) -> None:
        id_med = self._id_c.get().strip().upper()
        if not id_med:
            self._estado_w_c.mostrar("Ingrese un ID para consultar", "error")
            return
        try:
            m = self.controller.obtener_medicion_por_id(id_med)
        except Exception as e:
            self._estado_w_c.mostrar(f"Error: {e}", "error")
            return
        if m is None:
            self._res_c.set("—")
            self._estado_w_c.mostrar("Medicion no encontrada", "error")
            return
        self._res_c.set(
            f"ID: {m.id}  |  Estacion: {m.id_estacion}  |  DANE: {m.codigo_dane_municipio}"
            f"  |  Fecha: {m.fecha.date().isoformat()}  |  Valor: {m.medicion}"
            f"  |  Nivel ICA: {m.nivel}  |  Origen: {m.origen}"
        )
        self._estado_w_c.mostrar("Medicion encontrada", "success")

    # ─── Actualizar ─────────────────────────────────────────────────
    def _tab_actualizar(self, nb: ttk.Notebook) -> None:
        frame = ttk.Frame(nb, padding=12)
        nb.add(frame, text="  Actualizar medicion  ")

        ttk.Label(frame, text="Solo mediciones MANUALES pueden actualizarse. Deje campos vacios para no cambiar.",
                  foreground="#6b7280").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

        self._id_u = tk.StringVar()
        self._dane_u = tk.StringVar()
        self._est_u = tk.StringVar()
        self._fecha_u = tk.StringVar()
        self._valor_u = tk.StringVar()

        ttk.Label(frame, text="ID medicion").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        self._cb_actualizar = ttk.Combobox(frame, textvariable=self._id_u, width=30,
                                           postcommand=lambda: self._cargar_ids_medicion(self._cb_actualizar))
        self._cb_actualizar.grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(frame, text="Nuevo codigo DANE").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=4)
        self._cb_dane_u = ttk.Combobox(frame, textvariable=self._dane_u, width=30,
                                       postcommand=lambda: self._cargar_municipios(self._cb_dane_u))
        self._cb_dane_u.grid(row=2, column=1, sticky="ew", pady=4)

        ttk.Label(frame, text="Nueva ID estacion").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=4)
        self._cb_est_u = ttk.Combobox(frame, textvariable=self._est_u, width=30,
                                      postcommand=lambda: self._cargar_estaciones(self._cb_est_u))
        self._cb_est_u.grid(row=3, column=1, sticky="ew", pady=4)

        ttk.Label(frame, text="Nueva fecha (YYYY-MM-DD)").grid(row=4, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(frame, textvariable=self._fecha_u, width=30).grid(row=4, column=1, sticky="ew", pady=4)

        ttk.Label(frame, text="Nuevo valor").grid(row=5, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(frame, textvariable=self._valor_u, width=30).grid(row=5, column=1, sticky="ew", pady=4)

        ttk.Button(frame, text="Actualizar", command=self._actualizar).grid(row=6, column=0, columnspan=2, sticky="w", pady=(10, 4))
        self._estado_w_u = EstadoWidget(frame)
        self._estado_w_u.label.grid(row=7, column=0, columnspan=2, sticky="w", pady=(8, 0))
        frame.columnconfigure(1, weight=1)

    def _actualizar(self) -> None:
        id_med = self._id_u.get().strip().upper()
        if not id_med:
            self._estado_w_u.mostrar("Seleccione un ID de medicion", "error")
            return

        if not messagebox.askyesno("Confirmar", f"Actualizar medicion '{id_med}'?"):
            self._estado_w_u.mostrar("Operacion cancelada", "info")
            return

        kwargs = {}
        if self._dane_u.get().strip():
            kwargs["codigo_dane_municipio"] = self._dane_u.get().strip().upper()
        if self._est_u.get().strip():
            kwargs["id_estacion"] = self._est_u.get().strip().upper()
        if self._fecha_u.get().strip():
            try:
                kwargs["fecha"] = datetime.fromisoformat(self._fecha_u.get().strip())
            except ValueError:
                self._estado_w_u.mostrar("Fecha invalida, use YYYY-MM-DD", "error")
                return
        if self._valor_u.get().strip():
            try:
                kwargs["medicion"] = float(self._valor_u.get().strip())
            except ValueError:
                self._estado_w_u.mostrar("Valor debe ser numerico", "error")
                return

        self._view.usar(self._estado_w_u)
        actualizada = self.controller.actualizar_medicion(id_med, **kwargs)
        if actualizada is None:
            return
        self.refrescar()

    # ─── Eliminar ───────────────────────────────────────────────────
    def _tab_eliminar(self, nb: ttk.Notebook) -> None:
        frame = ttk.Frame(nb, padding=12)
        nb.add(frame, text="  Eliminar medicion  ")

        ttk.Label(frame, text="Solo mediciones MANUALES pueden eliminarse.",
                  foreground="#6b7280").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        self._id_d = tk.StringVar()
        ttk.Label(frame, text="ID medicion").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        self._cb_eliminar = ttk.Combobox(frame, textvariable=self._id_d, width=30,
                                         postcommand=lambda: self._cargar_ids_medicion(self._cb_eliminar))
        self._cb_eliminar.grid(row=1, column=1, sticky="ew", pady=4)
        ttk.Button(frame, text="Eliminar", command=self._eliminar).grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 4))

        self._estado_w_d = EstadoWidget(frame)
        self._estado_w_d.label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(8, 0))
        frame.columnconfigure(1, weight=1)

    def _eliminar(self) -> None:
        id_med = self._id_d.get().strip().upper()
        if not id_med:
            self._estado_w_d.mostrar("Seleccione un ID para eliminar", "error")
            return
        if not messagebox.askyesno("Confirmar", f"Eliminar medicion '{id_med}'?"):
            self._estado_w_d.mostrar("Operacion cancelada", "info")
            return

        self._view.usar(self._estado_w_d)
        self.controller.eliminar_medicion(id_med)
        if not self._view.exito:
            return
        self._id_d.set("")
        self.refrescar()

    # ─── Helpers combobox ───────────────────────────────────────────
    def _cargar_municipios(self, cb: ttk.Combobox) -> None:
        try:
            cb["values"] = [m.id_municipio for m in self.municipio_controller.listar_municipios()]
        except Exception:
            cb["values"] = []

    def _cargar_estaciones(self, cb: ttk.Combobox) -> None:
        try:
            cb["values"] = [e.id_estacion for e in self.estacion_controller.listar_estaciones()]
        except Exception:
            cb["values"] = []

    def _cargar_ids_medicion(self, cb: ttk.Combobox) -> None:
        try:
            cb["values"] = [m.id for m in self.controller.obtener_mediciones()]
        except Exception:
            cb["values"] = []
