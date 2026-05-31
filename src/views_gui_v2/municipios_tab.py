import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers.municipio_controller import MunicipioController
from src.exceptions.municipio_exceptions import (
    DatosMunicipioInvalidosError,
    MunicipioNoEncontradoError,
    ReglaNegocioMunicipioError,
)

class MunicipiosTab:
    def __init__(self, parent: ttk.Frame, controller: MunicipioController = None) -> None:
        self.controller = controller if controller else MunicipioController()
        
        self.frame = ttk.Frame(parent, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self._crear_widgets_estado()
        self._crear_formulario()
        self._crear_botones()
        self._crear_tabla()
        
        self.cargar_datos()

    def _crear_widgets_estado(self):
        """Crea un panel de resumen (Widgets de Estado) en la parte superior."""
        self.frame_widgets = ttk.LabelFrame(self.frame, text="Resumen de Municipios", padding="10")
        self.frame_widgets.pack(fill=tk.X, pady=5)

        self.var_total = tk.StringVar(value="Total: 0")
        self.var_activos = tk.StringVar(value="Activos: 0")
        self.var_inactivos = tk.StringVar(value="Inactivos: 0")

        ttk.Label(self.frame_widgets, textvariable=self.var_total, font=("Arial", 11, "bold")).pack(side=tk.LEFT, expand=True)
        ttk.Label(self.frame_widgets, textvariable=self.var_activos, font=("Arial", 11, "bold"), foreground="green").pack(side=tk.LEFT, expand=True)
        ttk.Label(self.frame_widgets, textvariable=self.var_inactivos, font=("Arial", 11, "bold"), foreground="red").pack(side=tk.LEFT, expand=True)

    def actualizar_widgets(self, municipios):
        """Calcula y actualiza las métricas de los widgets según los datos actuales."""
        total = len(municipios)
        activos = sum(1 for m in municipios if m.estado == "Activo")
        inactivos = total - activos

        self.var_total.set(f"Total: {total}")
        self.var_activos.set(f"Activos: {activos}")
        self.var_inactivos.set(f"Inactivos: {inactivos}")

    def _crear_formulario(self):
        form_frame = ttk.LabelFrame(self.frame, text="Datos del Municipio", padding="10")
        form_frame.pack(fill=tk.X, pady=5)

        ttk.Label(form_frame, text="ID Municipio:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_id = ttk.Entry(form_frame)
        self.entry_id.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(form_frame)
        self.entry_nombre.grid(row=0, column=3, sticky=tk.EW, padx=5, pady=5)

        ttk.Label(form_frame, text="Departamento:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_depto = ttk.Entry(form_frame)
        self.entry_depto.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        ttk.Label(form_frame, text="Región:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.entry_region = ttk.Entry(form_frame)
        self.entry_region.grid(row=1, column=3, sticky=tk.EW, padx=5, pady=5)

        ttk.Label(form_frame, text="Estado:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_estado = ttk.Combobox(form_frame, values=["Activo", "Inactivo"], state="readonly")
        self.combo_estado.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        self.combo_estado.set("Activo")

    def _crear_botones(self):
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="Crear", command=self.crear).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_campos).pack(side=tk.LEFT, padx=5)

    def _crear_tabla(self):
        columns = ("ID", "Nombre", "Departamento", "Región", "Estado")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
            
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            municipios = self.controller.listar_municipios()
            self.actualizar_widgets(municipios)
            
            for m in municipios:
                self.tree.insert("", tk.END, values=(m.id_municipio, m.nombre, m.departamento, m.region, m.estado))
        except Exception as e:
            messagebox.showerror("Error", f"Asegúrate de ejecutar desde main.py. Error: {str(e)}")

    def crear(self):
        try:
            self.controller.crear_municipio(
                self.entry_id.get(), self.entry_nombre.get(), self.entry_depto.get(),
                self.entry_region.get(), self.combo_estado.get()
            )
            messagebox.showinfo("Éxito", "Municipio creado. Se notificó por correo.")
            self.cargar_datos()
            self.limpiar_campos()
        except (DatosMunicipioInvalidosError, ReglaNegocioMunicipioError) as e:
            messagebox.showwarning("Validación", str(e))

    def actualizar(self):
        try:
            self.controller.actualizar_municipio(
                self.entry_id.get(), self.entry_nombre.get(), self.entry_depto.get(),
                self.entry_region.get(), self.combo_estado.get()
            )
            messagebox.showinfo("Éxito", "Municipio actualizado.")
            self.cargar_datos()
            self.limpiar_campos()
        except (DatosMunicipioInvalidosError, MunicipioNoEncontradoError) as e:
            messagebox.showwarning("Atención", str(e))

    def eliminar(self):
        id_mun = self.entry_id.get()
        if not id_mun:
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar municipio {id_mun}?"):
            try:
                self.controller.eliminar_municipio(id_mun)
                messagebox.showinfo("Éxito", "Municipio eliminado.")
                self.cargar_datos()
                self.limpiar_campos()
            except (ReglaNegocioMunicipioError, MunicipioNoEncontradoError) as e:
                messagebox.showerror("Error", str(e))

    def seleccionar_fila(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, "values")
            self.limpiar_campos()
            self.entry_id.insert(0, values[0])
            self.entry_id.config(state="readonly")
            self.entry_nombre.insert(0, values[1])
            self.entry_depto.insert(0, values[2])
            self.entry_region.insert(0, values[3])
            self.combo_estado.set(values[4])

    def limpiar_campos(self):
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_depto.delete(0, tk.END)
        self.entry_region.delete(0, tk.END)
        self.combo_estado.set("Activo")