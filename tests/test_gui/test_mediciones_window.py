"""Pruebas basicas de la vista GUI de mediciones."""

from datetime import datetime
import tkinter as tk

import pytest

from src.models.medicion_calidad_aire import MedicionCalidadAirePM
from src.views_gui.mediciones_window import MedicionesWindow


class MedicionesControllerDoble:
    def __init__(self):
        self._items = []

    def registrar_medicion(self, datos: dict[str, str]):
        item = MedicionCalidadAirePM(
            id=datos["id"],
            codigo_dane_municipio=datos["codigo_dane_municipio"],
            id_estacion=datos["id_estacion"],
            fecha=datetime.fromisoformat(datos["fecha"]),
            diametro_aerodinamico=datos["diametro_aerodinamico"],
            medicion=float(datos["medicion"]),
            origen="MANUAL",
        )
        self._items.append(item)
        return item

    def listar(self):
        return list(self._items)


@pytest.fixture(scope="module")
def root_tk():
    try:
        root = tk.Tk()
    except tk.TclError as error:
        pytest.skip(f"Tkinter no disponible en este entorno: {error}")
    root.withdraw()
    yield root
    root.destroy()


def _crear_ventana(root_tk):
    contenedor = tk.Toplevel(root_tk)
    controller = MedicionesControllerDoble()
    ventana = MedicionesWindow(contenedor, controller=controller)
    return contenedor, controller, ventana


def test_mediciones_window_valida_rango_y_formato_numerico(root_tk):
    contenedor, controller, ventana = _crear_ventana(root_tk)

    ventana.id_var.set("MED001")
    ventana.codigo_dane_var.set("11001")
    ventana.id_estacion_var.set("EST001")
    ventana.fecha_var.set("2026-05-24")
    ventana.medicion_var.set("abc")

    guardado = ventana.registrar_medicion()

    assert guardado is False
    assert len(controller.listar()) == 0
    assert "numerica" in ventana.estado.valor().lower()
    contenedor.destroy()


def test_mediciones_window_muestra_clasificacion_visible(root_tk):
    contenedor, controller, ventana = _crear_ventana(root_tk)

    ventana.id_var.set("MED002")
    ventana.codigo_dane_var.set("11001")
    ventana.id_estacion_var.set("EST001")
    ventana.fecha_var.set("2026-05-24")
    ventana.medicion_var.set("200")
    ventana.diametro_var.set("PM2.5")

    guardado = ventana.registrar_medicion()

    assert guardado is True
    assert len(controller.listar()) == 1
    assert ventana.clasificacion_var.get() == "Clasificacion: Alto"
    assert len(ventana.tabla.get_children()) == 1
    contenedor.destroy()
