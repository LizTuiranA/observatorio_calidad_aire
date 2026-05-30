"""Paquete shim para `views_gui_v2`.

Contiene reexports mínimos para soportar la transición entre `views_gui`
y `views_gui_v2`. Estos módulos delegan en las implementaciones existentes
de `src.views_gui` para que la ejecución de la "v2" sea inmediata.
"""

__all__ = [
    "alertas_tab",
    "estaciones_tab",
    "mediciones_tab",
    "municipios_tab",
    "widgets_estado",
]
