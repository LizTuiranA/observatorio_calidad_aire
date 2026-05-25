"""Pruebas basicas del contenedor principal GUI."""

import tkinter as tk
from types import SimpleNamespace

import pytest

from src.views_gui.app_window import AppWindow


@pytest.fixture(scope="module")
def root_tk():
    try:
        root = tk.Tk()
    except tk.TclError as error:
        pytest.skip(f"Tkinter no disponible en este entorno: {error}")
    root.withdraw()
    yield root
    root.destroy()


def test_app_window_abre_modulo_desde_menu(root_tk, monkeypatch):
    contenedor = tk.Toplevel(root_tk)
    app = AppWindow(contenedor)

    ventanas_abiertas = []

    class VentanaDummy:
        def __init__(self, child):
            ventanas_abiertas.append(child)

    modulo_dummy = SimpleNamespace(AlertasWindow=VentanaDummy)
    monkeypatch.setattr("src.views_gui.app_window.importlib.import_module", lambda _ruta: modulo_dummy)

    abierto = app.abrir_modulo("Alertas")

    assert abierto is True
    assert len(ventanas_abiertas) == 1
    assert "abierto correctamente" in app.estado.valor().lower()
    contenedor.destroy()


def test_app_window_maneja_error_de_carga_sin_bloquear(root_tk, monkeypatch):
    contenedor = tk.Toplevel(root_tk)
    app = AppWindow(contenedor)

    def _falla_import(_ruta):
        raise ImportError("modulo no disponible")

    monkeypatch.setattr("src.views_gui.app_window.importlib.import_module", _falla_import)

    abierto = app.abrir_modulo("Estaciones")

    assert abierto is False
    assert "error al abrir" in app.estado.valor().lower()

    monkeypatch.setattr("src.views_gui.app_window.messagebox.askyesno", lambda *_args, **_kwargs: False)
    cerrado = app.cerrar_aplicacion()
    assert cerrado is False
    assert "cancelada" in app.estado.valor().lower()
    contenedor.destroy()
