"""Pruebas basicas de la vista GUI de estaciones."""

import tkinter as tk

import pytest

from src.models.estacion_ambiental import EstacionAmbiental
from src.views_gui.estaciones_window import EstacionesWindow


class EstacionControllerDoble:
    def __init__(self):
        self._registros = []

    def crear_estacion(self, id_estacion, nombre, municipio, tipo_estacion, estado):
        estacion = EstacionAmbiental(id_estacion, nombre, municipio, tipo_estacion, estado)
        self._registros.append(estacion)
        return estacion

    def actualizar_estacion(self, id_estacion, nombre, municipio, tipo_estacion, estado):
        for i, estacion in enumerate(self._registros):
            if estacion.id_estacion == id_estacion:
                self._registros[i] = EstacionAmbiental(id_estacion, nombre, municipio, tipo_estacion, estado)
                return self._registros[i]
        raise ValueError("Estacion no encontrada")

    def listar_estaciones(self):
        return list(self._registros)


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
    controller = EstacionControllerDoble()
    ventana = EstacionesWindow(contenedor, controller=controller)
    return contenedor, controller, ventana


def test_estaciones_window_crea_estacion_y_refresca_lista(root_tk):
    contenedor, controller, ventana = _crear_ventana(root_tk)

    ventana.id_estacion_var.set("EST900")
    ventana.nombre_var.set("Centro")
    ventana.municipio_var.set("Bogota")
    ventana.tipo_var.set("Fija")
    ventana.estado_var.set("Activa")

    guardado = ventana.crear_estacion()

    assert guardado is True
    assert len(controller.listar_estaciones()) == 1
    assert len(ventana.tabla.get_children()) == 1
    assert "creada correctamente" in ventana.estado.valor().lower()
    contenedor.destroy()


def test_estaciones_window_actualiza_estacion_con_confirmacion(root_tk, monkeypatch):
    contenedor, controller, ventana = _crear_ventana(root_tk)
    controller.crear_estacion("EST901", "Norte", "Bogota", "Movil", "Activa")
    ventana.refrescar_lista()

    monkeypatch.setattr("src.views_gui.estaciones_window.messagebox.askyesno", lambda *_args, **_kwargs: True)

    ventana.id_estacion_var.set("EST901")
    ventana.nombre_var.set("Norte Actualizada")
    ventana.municipio_var.set("Bogota")
    ventana.tipo_var.set("Movil")
    ventana.estado_var.set("Inactiva")

    actualizado = ventana.actualizar_estacion()

    assert actualizado is True
    assert controller.listar_estaciones()[0].nombre == "Norte Actualizada"
    assert controller.listar_estaciones()[0].estado == "Inactiva"
    assert "actualizada correctamente" in ventana.estado.valor().lower()
    contenedor.destroy()
