# Evidencia GUI Liz - Actividad 8

## Datos del integrante
- Nombre: Liz Tuiran
- Correo: liz.tuiran@unisalle.edu.co
- Documento: Pendiente completar

## Bloque implementado
- Vista GUI de alertas con Tkinter.
- Archivos principales:
  - `src/views_gui/alertas_window.py`
  - `src/views_gui/widgets_estado.py`
  - `tests/test_gui/test_alertas_window.py`

## Como ejecutar la GUI
1. Activar entorno virtual.
2. Ejecutar:

```bash
python -m src.views_gui.alertas_window
```

## Evidencia de pruebas
Comando ejecutado:

```bash
python -m pytest -v tests/test_gui/test_alertas_window.py
```

Resultado esperado:
- 2 pruebas en estado `PASSED`.

## Mapeo de heuristicas de Nielsen
| Heuristica | Implementacion | Ubicacion |
| --- | --- | --- |
| Visibilidad del estado del sistema | Mensajes "Guardando alerta...", "Alerta guardada correctamente" y mensajes de error visibles en la ventana. | `src/views_gui/alertas_window.py` + `src/views_gui/widgets_estado.py` |
| Prevencion de errores | Validacion previa de campos obligatorios; bloquea guardado si faltan datos. | `validar_campos_obligatorios` y `guardar_alerta` en `src/views_gui/alertas_window.py` |
| Consistencia y estandares | Etiquetas, boton primario de guardado y boton de limpiar con estilo uniforme usando `ttk`. | `src/views_gui/alertas_window.py` |
| Control y libertad del usuario | Boton "Limpiar" para reiniciar formulario sin cerrar ventana. | `limpiar_formulario` en `src/views_gui/alertas_window.py` |
| Reconocer antes que recordar | Uso de `Combobox` para `nivel` y `estado` en lugar de texto libre. | `src/views_gui/alertas_window.py` |

## Capturas

### Formulario de alertas

![Formulario de alertas](./Formulario.jpg)

### Guardado exitoso

![Formulario guardado](./Formulario%20guardado.jpg)

### Validacion de errores

![Error de validacion 1](./Alerta%20erro%20de%20validaci%C3%B3n%201.jpg)

![Error de validacion 2](./Alerta%20erro%20de%20validaci%C3%B3n%202.jpg)

![Error de validacion 3](./Alerta%20erro%20de%20validaci%C3%B3n%203.jpg)

## Riesgos y notas
- Si el sistema se ejecuta en entorno sin soporte grafico, Tkinter puede fallar al iniciar ventana.
- Para pruebas automatizadas en CI sin pantalla puede requerirse estrategia de virtual display.
