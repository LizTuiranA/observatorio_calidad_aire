# Evidencia GUI Jose - Actividad 8

## Datos del integrante
- Nombre: Jose Rojas

## Bloque implementado
- Contenedor principal GUI y navegacion entre modulos.
- Archivos:
  - `src/views_gui/app_window.py`
  - `src/views_gui/run_gui.py`
  - `tests/test_gui/test_app_window.py`

## Como ejecutar
```bash
python -m src.views_gui.run_gui
```

## Pruebas ejecutadas
```bash
python -m pytest -v tests/test_gui/test_app_window.py
python -m pytest -v tests/test_gui
python -m pytest -v
```

## Heuristicas de Nielsen aplicadas
| Heuristica | Implementacion | Ubicacion |
| --- | --- | --- |
| Control y libertad del usuario | Navegacion clara por botones y confirmacion de salida con opcion de cancelar. | `src/views_gui/app_window.py` |
| Consistencia global | Misma familia de widgets `ttk`, estilo de botones y mensajes de estado compartidos. | `src/views_gui/app_window.py` + `src/views_gui/widgets_estado.py` |
| Visibilidad del estado | Mensajes de estado al abrir modulo, exito de apertura o error de carga. | `src/views_gui/app_window.py` |

## Conflictos de integracion (QA)
- Si un modulo aun no existe (`estaciones_window` o `mediciones_window`), la app no se cae: muestra error en estado y sigue operativa.
- En ambientes sin GUI, Tkinter puede requerir estrategia de skip/entorno adecuado para pruebas.

## Capturas
- Pendiente adjuntar:
  - `entregables/actividad8/jose/capturas/gui_app_menu.png`
  - `entregables/actividad8/jose/capturas/gui_app_error_carga.png`
  - `entregables/actividad8/jose/capturas/gui_app_confirmacion_salida.png`
