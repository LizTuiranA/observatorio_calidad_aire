# Evidencia GUI Daniel - Actividad 8

## Datos del integrante
- Nombre: Daniel (completar nombre completo)
- Correo: completar
- Documento: completar

## Bloque implementado
- Vista GUI de mediciones con Tkinter.
- Archivos:
  - `src/views_gui/mediciones_window.py`
  - `tests/test_gui/test_mediciones_window.py`

## Como ejecutar
```bash
python -m src.views_gui.mediciones_window
```

## Pruebas ejecutadas
```bash
python -m pytest -v tests/test_gui/test_mediciones_window.py
```

Resultado esperado:
- 2 pruebas en estado `PASSED`.

## Heuristicas de Nielsen aplicadas
| Heuristica | Implementacion | Ubicacion |
| --- | --- | --- |
| Prevencion de errores | Validacion previa de campos obligatorios, formato numerico y rango de medicion antes de registrar. | `src/views_gui/mediciones_window.py` |
| Visibilidad del estado del sistema | Mensajes inmediatos de estado (`Registrando...`, exito, error) y clasificacion visible en pantalla. | `src/views_gui/mediciones_window.py` |
| Reconocer antes que recordar | Placeholders/sugerencias de formato junto a los campos y combobox para diametro PM. | `src/views_gui/mediciones_window.py` |

## Capturas
- Pendiente adjuntar:
  - `entregables/actividad8/daniel/capturas/gui_mediciones_formulario.png`
  - `entregables/actividad8/daniel/capturas/gui_mediciones_clasificacion.png`
  - `entregables/actividad8/daniel/capturas/gui_mediciones_validacion_error.png`

## Riesgos
- En entorno sin soporte grafico, Tkinter puede no iniciar.
- Si se ejecuta en CI headless, puede requerir display virtual para pruebas GUI.
