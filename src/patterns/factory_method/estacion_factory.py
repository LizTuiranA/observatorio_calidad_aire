"""Factory Method para crear entidades de estaciones ambientales."""

from src.models.estacion_ambiental import EstacionAmbiental


class EstacionFactory:
    """Centraliza la creacion de estaciones para desacoplar la capa de uso."""

    @staticmethod
    def crear(
        id_estacion: str,
        nombre: str,
        municipio: str,
        tipo_estacion: str,
        estado: str,
    ) -> EstacionAmbiental:
        """Crea una estacion aplicando las validaciones del modelo."""
        return EstacionAmbiental(
            id_estacion=id_estacion,
            nombre=nombre,
            municipio=municipio,
            tipo_estacion=tipo_estacion,
            estado=estado,
        )
