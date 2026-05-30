"""Patron Decorator (GoF) que agrega notificacion por email al repositorio de alertas.

Envuelve un repositorio concreto de alertas y, tras cada operacion de escritura
exitosa (crear/actualizar/eliminar), envia una notificacion mediante EmailService.
Los metodos de lectura solo delegan.

A diferencia de mediciones, no existe una interfaz `IAlertaRepository`, asi que este
decorator actua como proxy transparente: cualquier atributo distinto de los metodos CRUD
(por ejemplo `data_file` o `_asegurar_archivo`) se reenvia al repositorio envuelto.
"""

from src.models.alerta_ambiental import AlertaAmbiental
from src.services.email_service import EmailService


class EmailDecoratorAlerta:
    """Decorator que notifica por correo las operaciones CRUD de alertas."""

    def __init__(self, wrapped, email_service: EmailService) -> None:
        object.__setattr__(self, "_wrapped", wrapped)
        object.__setattr__(self, "_email", email_service)

    def crear_alerta(self, alerta: AlertaAmbiental) -> AlertaAmbiental:
        resultado = self._wrapped.crear_alerta(alerta)
        self._email.enviar_notificacion(
            "creación",
            f"Alerta {alerta.id_alerta} registrada (nivel {alerta.nivel})",
            entidad="Alerta",
        )
        return resultado

    def actualizar_alerta(self, id_alerta: str, alerta: AlertaAmbiental) -> AlertaAmbiental:
        resultado = self._wrapped.actualizar_alerta(id_alerta, alerta)
        self._email.enviar_notificacion(
            "actualización",
            f"Alerta {id_alerta} actualizada",
            entidad="Alerta",
        )
        return resultado

    def eliminar_alerta(self, id_alerta: str) -> bool:
        resultado = self._wrapped.eliminar_alerta(id_alerta)
        self._email.enviar_notificacion(
            "eliminación",
            f"Alerta {id_alerta} eliminada",
            entidad="Alerta",
        )
        return resultado

    def listar_alertas(self):
        return self._wrapped.listar_alertas()

    def buscar_alerta_por_id(self, id_alerta: str):
        return self._wrapped.buscar_alerta_por_id(id_alerta)

    def __getattr__(self, name):
        """Reenvia atributos no definidos aqui al repositorio envuelto."""
        return getattr(self._wrapped, name)

    def __setattr__(self, name, value):
        """Reenvia la asignacion de atributos al repositorio envuelto."""
        setattr(self._wrapped, name, value)
