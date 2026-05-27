"""Patron Decorator (GoF) que agrega notificacion por email a IMedicionRepository.

Envuelve un repositorio concreto y, tras cada operacion de escritura
exitosa (crear/actualizar/eliminar), envia una notificacion mediante
EmailService. Los metodos de lectura solo delegan.
"""

from src.models.medicion_calidad_aire import MedicionCalidadAire
from src.repositories.medicion_calidad_aire_repository import IMedicionRepository
from src.services.email_service import EmailService


class EmailDecoratorMedicion(IMedicionRepository):
    """Decorator que notifica por correo las operaciones CRUD de mediciones."""

    def __init__(
        self,
        wrapped: IMedicionRepository,
        email_service: EmailService,
    ) -> None:
        self._wrapped = wrapped
        self._email = email_service

    def crear_medicion(self, medicion: MedicionCalidadAire) -> MedicionCalidadAire:
        resultado = self._wrapped.crear_medicion(medicion)
        self._email.enviar_notificacion(
            "creación", f"Medición {medicion.id} registrada", entidad="Medición"
        )
        return resultado

    def actualizar_medicion(self, medicion: MedicionCalidadAire) -> MedicionCalidadAire:
        resultado = self._wrapped.actualizar_medicion(medicion)
        self._email.enviar_notificacion(
            "actualización", f"Medición {medicion.id} actualizada", entidad="Medición"
        )
        return resultado

    def eliminar_medicion(self, medicion_id: str) -> bool:
        resultado = self._wrapped.eliminar_medicion(medicion_id)
        self._email.enviar_notificacion(
            "eliminación", f"Medición {medicion_id} eliminada", entidad="Medición"
        )
        return resultado

    def listar_mediciones(self) -> list[MedicionCalidadAire]:
        return self._wrapped.listar_mediciones()

    def buscar_medicion_por_id(self, medicion_id: str) -> MedicionCalidadAire | None:
        return self._wrapped.buscar_medicion_por_id(medicion_id)
