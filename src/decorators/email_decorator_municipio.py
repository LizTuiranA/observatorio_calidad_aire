"""Patrón Decorator (GoF) que agrega notificación por email a MunicipioRepository.

Envuelve un repositorio concreto de municipios y, tras cada operación de escritura
exitosa (crear/actualizar/eliminar), envía una notificación mediante EmailService.
Los métodos de lectura solo delegan.
"""

from src.models.municipio import Municipio
from src.repositories.municipio_repository import MunicipioRepository
from src.services.email_service import EmailService


class EmailDecoratorMunicipio:
    """Decorator que notifica por correo las operaciones CRUD de municipios."""

    def __init__(
        self,
        wrapped: MunicipioRepository,
        email_service: EmailService,
    ) -> None:
        self._wrapped = wrapped
        self._email = email_service

    def crear(self, municipio: Municipio) -> Municipio:
        """Crea un municipio y envía notificación de creación."""
        resultado = self._wrapped.crear(municipio)
        self._email.enviar_notificacion(
            "creación",
            f"Municipio {municipio.id_municipio} ({municipio.nombre}) registrado",
            entidad="Municipio",
        )
        return resultado

    def actualizar(self, id_municipio: str, municipio_actualizado: Municipio) -> Municipio | None:
        """Actualiza un municipio y envía notificación de actualización."""
        resultado = self._wrapped.actualizar(id_municipio, municipio_actualizado)
        if resultado:
            self._email.enviar_notificacion(
                "actualización",
                f"Municipio {id_municipio} ({municipio_actualizado.nombre}) actualizado",
                entidad="Municipio",
            )
        return resultado

    def eliminar(self, id_municipio: str) -> bool:
        """Elimina un municipio y envía notificación de eliminación."""
        resultado = self._wrapped.eliminar(id_municipio)
        if resultado:
            self._email.enviar_notificacion(
                "eliminación",
                f"Municipio {id_municipio} eliminado",
                entidad="Municipio",
            )
        return resultado

    def listar(self) -> list[Municipio]:
        """Lista todos los municipios."""
        return self._wrapped.listar()

    def buscar_por_id(self, id_municipio: str) -> Municipio | None:
        """Busca un municipio por ID."""
        return self._wrapped.buscar_por_id(id_municipio)
