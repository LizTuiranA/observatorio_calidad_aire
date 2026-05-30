"""Controlador para operaciones CRUD de EstacionAmbiental."""

from src.patterns.factory_method.estacion_factory import EstacionFactory
from src.repositories.estacion_repository import EstacionRepository
from src.decorators.email_decorator_estacion import EmailDecoratorEstacion
from src.services.email_service import EmailService


class EstacionController:
    """Coordina modelo de estaciones y repositorio."""

    def __init__(self, repository=None):
        # Por defecto, envolver el repositorio con el decorator que notifica por email
        self.repository = (
            repository
            or EmailDecoratorEstacion(EstacionRepository(), EmailService())
        )

    def crear_estacion(self, id_estacion, nombre, municipio, tipo_estacion, estado):
        estacion = EstacionFactory.crear(
            id_estacion,
            nombre,
            municipio,
            tipo_estacion,
            estado,
        )
        return self.repository.crear(estacion)

    def listar_estaciones(self):
        return self.repository.listar()

    def buscar_estacion(self, id_estacion):
        return self.repository.buscar(id_estacion)

    def actualizar_estacion(self, id_estacion, nombre, municipio, tipo_estacion, estado):
        estacion = EstacionFactory.crear(
            id_estacion,
            nombre,
            municipio,
            tipo_estacion,
            estado,
        )
        return self.repository.actualizar(estacion)

    def eliminar_estacion(self, id_estacion):
        return self.repository.eliminar(id_estacion)
