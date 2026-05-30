"""Decorator que añade notificaciones por email a las operaciones CRUD de estaciones."""

from src.models.estacion_ambiental import EstacionAmbiental
from src.repositories.estacion_repository import EstacionRepository
from src.services.email_service import EmailService


class EmailDecoratorEstacion:
    """Envuelve un EstacionRepository y envía emails tras operaciones de escritura."""

    def __init__(self, wrapped: EstacionRepository, email_service: EmailService) -> None:
        self._wrapped = wrapped
        self._email = email_service

    def crear(self, estacion: EstacionAmbiental) -> EstacionAmbiental:
        resultado = self._wrapped.crear(estacion)
        self._email.enviar_notificacion(
            "creación",
            f"Estación {estacion.id_estacion} ({estacion.nombre}) registrada",
            entidad="EstacionAmbiental",
        )
        return resultado

    def listar(self) -> list[EstacionAmbiental]:
        return self._wrapped.listar()

    def buscar(self, id_estacion: str) -> EstacionAmbiental | None:
        return self._wrapped.buscar(id_estacion)

    def actualizar(self, estacion_actualizada: EstacionAmbiental) -> EstacionAmbiental:
        resultado = self._wrapped.actualizar(estacion_actualizada)
        if resultado:
            self._email.enviar_notificacion(
                "actualización",
                f"Estación {estacion_actualizada.id_estacion} ({estacion_actualizada.nombre}) actualizada",
                entidad="EstacionAmbiental",
            )
        return resultado

    def eliminar(self, id_estacion: str) -> bool:
        resultado = self._wrapped.eliminar(id_estacion)
        if resultado:
            self._email.enviar_notificacion(
                "eliminación",
                f"Estación {id_estacion} eliminada",
                entidad="EstacionAmbiental",
            )
        return resultado
