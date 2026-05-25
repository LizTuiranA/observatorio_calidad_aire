"""Servicio base para operaciones de alertas sin notificacion."""


class EmailService:
    """Simula la operacion principal de crear/actualizar una alerta."""

    def crear_o_actualizar_alerta(self, alerta_id: str, accion: str) -> str:
        """Ejecuta la operacion principal y retorna un mensaje simple."""
        return f"Alerta {alerta_id} {accion} correctamente"
