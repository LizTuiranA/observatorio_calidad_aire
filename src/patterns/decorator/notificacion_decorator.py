"""Decorator que agrega notificacion despues de la operacion base."""

from pathlib import Path


class NotificacionDecorator:
    """Extiende un servicio base para registrar notificaciones."""

    def __init__(self, servicio_base, log_file: str | Path | None = None) -> None:
        self._servicio_base = servicio_base
        self._log_file = Path(log_file) if log_file else None

    def crear_o_actualizar_alerta(self, alerta_id: str, accion: str) -> str:
        """Ejecuta la operacion base y luego registra la notificacion."""
        resultado = self._servicio_base.crear_o_actualizar_alerta(alerta_id, accion)
        self._registrar_notificacion(alerta_id, accion)
        return resultado

    def _registrar_notificacion(self, alerta_id: str, accion: str) -> None:
        mensaje = f"Notificacion enviada para alerta {alerta_id} tras {accion}"
        if self._log_file is None:
            return

        self._log_file.parent.mkdir(parents=True, exist_ok=True)
        with self._log_file.open("a", encoding="utf-8") as archivo:
            archivo.write(mensaje + "\n")
