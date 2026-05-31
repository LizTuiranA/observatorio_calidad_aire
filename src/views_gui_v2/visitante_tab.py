import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers.municipio_controller import MunicipioController
from src.controllers.estacion_controller import EstacionController
from src.controllers.medicion_calidad_aire_controller import MedicionController

class VisitanteTab:
    def __init__(self, parent: ttk.Frame) -> None:
        self.mun_ctrl = MunicipioController()
        self.est_ctrl = EstacionController()
        self.med_ctrl = MedicionController()
        
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
        
        # Único botón permitido en toda la interfaz de visitante
        ttk.Button(filtro_frame, text="Consultar", command=self.consultar_datos).pack(side=tk.LEFT, padx=15)

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
        cols_est = ("ID Estación", "Nombre", "Ubicación", "Estado")
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

    def cargar_datos_iniciales(self):
        """Carga la lista de municipios en el combobox y en la tabla principal."""
        try:
            municipios = self.mun_ctrl.listar_municipios()
            # Mapeo para facilitar el filtro por ID internamente
            self.mapa_municipios = {f"{m.nombre} ({m.id_municipio})": m.id_municipio for m in municipios}
            valores = ["Todos"] + list(self.mapa_municipios.keys())
            self.combo_municipios.config(values=valores)
            self.combo_municipios.set("Todos")
            
            # Llenar la tabla de municipios
            self._llenar_tabla_municipios(municipios)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos base: {str(e)}")

    def consultar_datos(self):
        """Filtra y muestra la información en las tablas según el municipio seleccionado."""
        # Primero limpiamos las tablas de estaciones y mediciones
        for item in self.tree_est.get_children(): self.tree_est.delete(item)
        for item in self.tree_med.get_children(): self.tree_med.delete(item)

        seleccion = self.combo_municipios.get()
        id_mun_filtro = None if seleccion == "Todos" else self.mapa_municipios.get(seleccion)

        if id_mun_filtro:
            mensaje = f"Filtrando estaciones y mediciones para el municipio ID: {id_mun_filtro}"
        else:
            mensaje = "Consultando todas las estaciones y mediciones en el sistema."
            
        messagebox.showinfo("Consulta de Visitante", mensaje + "\n(Las tablas se llenarán cuando se integren los controladores de tus compañeros)")

        estaciones = self.est_ctrl.listar_por_municipio(id_mun_filtro)
        for e in estaciones: self.tree_est.insert("", tk.END, values=(...))
        
        mediciones = self.med_ctrl.listar_por_municipio(id_mun_filtro)
        for m in mediciones: self.tree_med.insert("", tk.END, values=(...))

    def _llenar_tabla_municipios(self, municipios):
        for item in self.tree_mun.get_children():
            self.tree_mun.delete(item)
        for m in municipios:
            self.tree_mun.insert("", tk.END, values=(m.id_municipio, m.nombre, m.departamento, m.region, m.estado))