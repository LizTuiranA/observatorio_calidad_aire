"""Ventana Tkinter para registrar mediciones de calidad del aire."""

from datetime import datetime
import tkinter as tk
from tkinter import ttk

from src.exceptions.custom_exceptions import DatoInvalidoError
from src.factories.medicion_factory import MedicionFactory
from src.models.medicion_calidad_aire import MedicionCalidadAire, MedicionCalidadAirePM
from src.repositories.medicion_calidad_aire_repository import MedicionRepository
from src.views_gui.widgets_estado import EstadoWidget


def validar_obligatorios(campos: dict[str, str]) -> tuple[bool, str]:
    """Valida que todos los campos requeridos tengan valor."""
    for nombre, valor in campos.items():
        if not str(valor).strip():
            return False, f"El campo '{nombre}' es obligatorio"
    return True, ""


def validar_medicion_numerica(valor: str) -> tuple[bool, str, float | None]:
    """Valida formato y rango basico para medicion."""
    try:
        numero = float(valor)
    except ValueError:
        return False, "La medicion debe ser numerica", None

    if numero <= 0:
        return False, "La medicion debe ser mayor a 0", None
    if numero > 1000:
        return False, "La medicion parece fuera de rango (max 1000)", None
    return True, "", numero


def clasificacion_visible(nivel_ica: str) -> str:
    """Traduce nivel ICA tecnico a etiqueta simple bajo/medio/alto."""
    if nivel_ica in (MedicionCalidadAire.BUENA, MedicionCalidadAire.ACEPTABLE):
        return "Bajo"
    if nivel_ica in (MedicionCalidadAire.DANINA_SENSIBLES, MedicionCalidadAire.DANINA):
        return "Medio"
    return "Alto"


class MedicionesControllerGUI:
    """Adaptador simple para guardar/listar mediciones desde la GUI."""

    def __init__(self, repository: MedicionRepository | None = None) -> None:
        self.repository = repository or MedicionRepository()

    def registrar_medicion(self, datos: dict[str, str]):
        medicion = MedicionFactory.crear(
            "PM",
            id=datos["id"].strip().upper(),
            codigo_dane_municipio=datos["codigo_dane_municipio"].strip().upper(),
            id_estacion=datos["id_estacion"].strip().upper(),
            fecha=datetime.fromisoformat(datos["fecha"].strip()),
            diametro_aerodinamico=datos["diametro_aerodinamico"],
            medicion=float(datos["medicion"]),
            origen=MedicionCalidadAire.MANUAL,
        )
        return self.repository.crear_medicion(medicion)

    def listar(self):
        return self.repository.listar_mediciones()


class MedicionesWindow:
    """Formulario para registrar mediciones PM y ver clasificacion."""

    DIAMETROS = (MedicionCalidadAirePM.PM25, MedicionCalidadAirePM.PM10)

    def __init__(self, root: tk.Tk | tk.Toplevel, controller: MedicionesControllerGUI | None = None) -> None:
        self.root = root
        self.controller = controller or MedicionesControllerGUI()
        self.root.title("Registro de Mediciones")
        self._crear_variables()
        self._crear_layout()
        self.refrescar_lista()

    def _crear_variables(self) -> None:
        self.id_var = tk.StringVar()
        self.codigo_dane_var = tk.StringVar()
        self.id_estacion_var = tk.StringVar()
        self.fecha_var = tk.StringVar(value="2026-05-24")
        self.medicion_var = tk.StringVar(value="12.5")
        self.diametro_var = tk.StringVar(value=self.DIAMETROS[0])
        self.clasificacion_var = tk.StringVar(value="Clasificacion: -")

    def _crear_layout(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        etiquetas = [
            ("ID medicion", self.id_var, "Ej: MED001"),
            ("Codigo DANE", self.codigo_dane_var, "Ej: 11001"),
            ("ID estacion", self.id_estacion_var, "Ej: EST001"),
            ("Fecha (YYYY-MM-DD)", self.fecha_var, "Ej: 2026-05-24"),
            ("Valor medicion", self.medicion_var, "Ej: 12.5"),
        ]
        for idx, (texto, variable, ayuda) in enumerate(etiquetas):
            ttk.Label(frame, text=texto).grid(row=idx, column=0, sticky="w", padx=(0, 8), pady=4)
            ttk.Entry(frame, textvariable=variable, width=34).grid(row=idx, column=1, sticky="ew", pady=4)
            ttk.Label(frame, text=ayuda).grid(row=idx, column=2, sticky="w", pady=4)

        ttk.Label(frame, text="Diametro").grid(row=5, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Combobox(frame, textvariable=self.diametro_var, values=self.DIAMETROS, state="readonly").grid(
            row=5, column=1, sticky="ew", pady=4
        )

        botonera = ttk.Frame(frame)
        botonera.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(10, 6))
        ttk.Button(botonera, text="Registrar medicion", command=self.registrar_medicion).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(botonera, text="Limpiar", command=self.limpiar_formulario).grid(row=0, column=1)

        ttk.Label(frame, textvariable=self.clasificacion_var).grid(row=7, column=0, columnspan=3, sticky="w", pady=(2, 6))

        self.tabla = ttk.Treeview(
            frame,
            columns=("id", "fecha", "valor", "nivel", "clasificacion"),
            show="headings",
            height=8,
        )
        self.tabla.heading("id", text="ID")
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("valor", text="Valor")
        self.tabla.heading("nivel", text="Nivel ICA")
        self.tabla.heading("clasificacion", text="Clasificacion")
        self.tabla.grid(row=8, column=0, columnspan=3, sticky="nsew", pady=(4, 0))

        self.estado = EstadoWidget(frame)
        self.estado.label.grid(row=9, column=0, columnspan=3, sticky="w", pady=(8, 0))

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(8, weight=1)

    def _datos_formulario(self) -> dict[str, str]:
        return {
            "id": self.id_var.get(),
            "codigo_dane_municipio": self.codigo_dane_var.get(),
            "id_estacion": self.id_estacion_var.get(),
            "fecha": self.fecha_var.get(),
            "medicion": self.medicion_var.get(),
            "diametro_aerodinamico": self.diametro_var.get(),
        }

    def registrar_medicion(self) -> bool:
        self.estado.mostrar("Registrando medicion...", "info")
        datos = self._datos_formulario()

        valido, mensaje = validar_obligatorios(
            {
                "id": datos["id"],
                "codigo_dane_municipio": datos["codigo_dane_municipio"],
                "id_estacion": datos["id_estacion"],
                "fecha": datos["fecha"],
                "medicion": datos["medicion"],
            }
        )
        if not valido:
            self.estado.mostrar(mensaje, "error")
            return False

        ok_numero, msg_numero, numero = validar_medicion_numerica(datos["medicion"])
        if not ok_numero:
            self.estado.mostrar(msg_numero, "error")
            return False
        datos["medicion"] = str(numero)

        try:
            datetime.fromisoformat(datos["fecha"].strip())
        except ValueError:
            self.estado.mostrar("La fecha debe tener formato YYYY-MM-DD", "error")
            return False

        try:
            medicion = self.controller.registrar_medicion(datos)
        except (DatoInvalidoError, ValueError) as error:
            self.estado.mostrar(f"Error: {error}", "error")
            return False

        clasificacion = clasificacion_visible(medicion.nivel)
        self.clasificacion_var.set(f"Clasificacion: {clasificacion}")
        self.refrescar_lista()
        self.estado.mostrar("Medicion registrada correctamente", "success")
        return True

    def refrescar_lista(self) -> None:
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for medicion in self.controller.listar():
            clasificacion = clasificacion_visible(medicion.nivel)
            self.tabla.insert(
                "",
                "end",
                values=(
                    medicion.id,
                    medicion.fecha.date().isoformat(),
                    medicion.medicion,
                    medicion.nivel,
                    clasificacion,
                ),
            )

    def limpiar_formulario(self) -> None:
        self.id_var.set("")
        self.codigo_dane_var.set("")
        self.id_estacion_var.set("")
        self.fecha_var.set("2026-05-24")
        self.medicion_var.set("12.5")
        self.diametro_var.set(self.DIAMETROS[0])
        self.clasificacion_var.set("Clasificacion: -")
        self.estado.mostrar("Formulario limpio", "info")


def ejecutar() -> None:
    root = tk.Tk()
    MedicionesWindow(root)
    root.mainloop()


if __name__ == "__main__":
    ejecutar()
