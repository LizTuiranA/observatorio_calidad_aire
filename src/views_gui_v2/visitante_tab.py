import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers.municipio_controller import MunicipioController
from src.controllers.estacion_controller import EstacionController
from src.controllers.medicion_calidad_aire_controller import MedicionController
from src.controllers.alerta_controller import AlertaController

class VisitanteTab:
    def __init__(self, parent: ttk.Frame) -> None:
        # Instanciamos todos los controladores del equipo
        self.mun_ctrl = MunicipioController()
        self.est_ctrl = EstacionController()
        self.med_ctrl = MedicionController()
        self.ale_ctrl = AlertaController()
        
        self.frame = ttk.Frame(parent, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self._crear_filtros()
        self._crear_tablas()
        self.cargar_datos_iniciales()

    def _crear_filtros(self):
        """Crea un panel superior exclusivo para consultas y filtros."""
        filtro_frame = ttk.LabelFrame(self.frame, text="Consultar y Filtrar Información", padding="10")
        filtro_frame.pack(fill=tk.X, pady=5)

        ttk.Label(filtro_frame, text="Seleccione un Municipio:").pack(side=tk.LEFT, padx=5)
        self.combo_municipios = ttk.Combobox(filtro_frame, state="readonly", width=40)
        self.combo_municipios.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filtro_frame, text="Consultar / Refrescar", command=self.consultar_datos).pack(side=tk.LEFT, padx=15)

    def _crear_tablas(self):
        """Crea el sistema de pestañas para visualizar los datos en tablas."""
        notebook = ttk.Notebook(self.frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        # --- 1. Pestaña de Municipios ---
        frame_mun = ttk.Frame(notebook)
        notebook.add(frame_mun, text="Municipios")
        cols_mun = ("ID", "Nombre", "Departamento", "Región", "Estado")
        self.tree_mun = ttk.Treeview(frame_mun, columns=cols_mun, show="headings")
        for col in cols_mun: 
            self.tree_mun.heading(col, text=col)
            self.tree_mun.column(col, anchor=tk.CENTER)
        self.tree_mun.pack(fill=tk.BOTH, expand=True)

        # --- 2. Pestaña de Estaciones ---
        frame_est = ttk.Frame(notebook)
        notebook.add(frame_est, text="Estaciones")
        cols_est = ("ID Estación", "Nombre", "Municipio ID", "Estado")
        self.tree_est = ttk.Treeview(frame_est, columns=cols_est, show="headings")
        for col in cols_est: 
            self.tree_est.heading(col, text=col)
            self.tree_est.column(col, anchor=tk.CENTER)
        self.tree_est.pack(fill=tk.BOTH, expand=True)

        # --- 3. Pestaña de Mediciones ---
        frame_med = ttk.Frame(notebook)
        notebook.add(frame_med, text="Mediciones")
        cols_med = ("ID Medición", "Fecha", "Contaminante", "Valor")
        self.tree_med = ttk.Treeview(frame_med, columns=cols_med, show="headings")
        for col in cols_med: 
            self.tree_med.heading(col, text=col)
            self.tree_med.column(col, anchor=tk.CENTER)
        self.tree_med.pack(fill=tk.BOTH, expand=True)

        # --- 4. Pestaña de Alertas ---
        frame_ale = ttk.Frame(notebook)
        notebook.add(frame_ale, text="Alertas Emitidas")
        cols_ale = ("ID Alerta", "Gravedad", "Fecha", "Medición ID")
        self.tree_ale = ttk.Treeview(frame_ale, columns=cols_ale, show="headings")
        for col in cols_ale: 
            self.tree_ale.heading(col, text=col)
            self.tree_ale.column(col, anchor=tk.CENTER)
        self.tree_ale.pack(fill=tk.BOTH, expand=True)

    def cargar_datos_iniciales(self):
        """Carga la lista de municipios en el combobox e invoca la primera consulta."""
        try:
            municipios = self.mun_ctrl.listar_municipios()
            self.mapa_municipios = {f"{m.nombre} ({m.id_municipio})": m.id_municipio for m in municipios}
            valores = ["Todos"] + list(self.mapa_municipios.keys())
            self.combo_municipios.config(values=valores)
            self.combo_municipios.set("Todos")
            
            self.consultar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos base: {str(e)}")

    def consultar_datos(self):
        """Filtra y muestra la información en todas las tablas según el municipio."""
        # Limpiar todas las tablas antes de llenarlas
        for item in self.tree_mun.get_children(): self.tree_mun.delete(item)
        for item in self.tree_est.get_children(): self.tree_est.delete(item)
        for item in self.tree_med.get_children(): self.tree_med.delete(item)
        for item in self.tree_ale.get_children(): self.tree_ale.delete(item)

        seleccion = self.combo_municipios.get()
        id_mun_filtro = None if seleccion == "Todos" else self.mapa_municipios.get(seleccion)

        try:
            # 1. Cargar Municipios
            municipios = self.mun_ctrl.listar_municipios()
            if id_mun_filtro:
                municipios = [m for m in municipios if m.id_municipio == id_mun_filtro]
            for m in municipios:
                self.tree_mun.insert("", tk.END, values=(m.id_municipio, m.nombre, m.departamento, m.region, m.estado))

            # 2. Cargar Estaciones (Corregido a listar_estaciones)
            estaciones = self.est_ctrl.listar_estaciones()
            if id_mun_filtro:
                estaciones = [e for e in estaciones if getattr(e, 'id_municipio', getattr(e, 'municipio', '')) == id_mun_filtro]
            for e in estaciones:
                self.tree_est.insert("", tk.END, values=(
                    getattr(e, 'id_estacion', ''), getattr(e, 'nombre', ''), 
                    getattr(e, 'id_municipio', getattr(e, 'municipio', '')), getattr(e, 'estado', '')
                ))

            # 3. Cargar Mediciones (Corregido a obtener_mediciones)
            mediciones = self.med_ctrl.obtener_mediciones()
            if id_mun_filtro:
                estaciones_ids = [getattr(e, 'id_estacion', '') for e in estaciones]
                mediciones = [m for m in mediciones if getattr(m, 'id_estacion', '') in estaciones_ids]
            for m in mediciones:
                self.tree_med.insert("", tk.END, values=(
                    getattr(m, 'id_medicion', getattr(m, 'id', '')), getattr(m, 'fecha', ''), 
                    getattr(m, 'contaminante', getattr(m, 'tipo', '')), getattr(m, 'valor', getattr(m, 'medicion', ''))
                ))

            # 4. Cargar Alertas (Corregido a listar_alertas)
            alertas = self.ale_ctrl.listar_alertas()
            if id_mun_filtro:
                mediciones_ids = [getattr(m, 'id_medicion', getattr(m, 'id', '')) for m in mediciones]
                alertas = [a for a in alertas if getattr(a, 'id_medicion', '') in mediciones_ids]
            for a in alertas:
                self.tree_ale.insert("", tk.END, values=(
                    getattr(a, 'id_alerta', ''), getattr(a, 'gravedad', getattr(a, 'nivel', '')), 
                    getattr(a, 'fecha', getattr(a, 'fecha_emision', '')), getattr(a, 'id_medicion', '')
                ))

        except Exception as e:
            messagebox.showwarning("Aviso", f"Error cruzando los datos: {e}\nRevisa que haya registros en los JSON.")