"""Factory Method para crear entidades de estaciones ambientales."""

from __future__ import annotations

from typing import Any

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

    @staticmethod
    def desde_dict(data: dict[str, Any]) -> EstacionAmbiental:
        """Crea una estacion a partir de un diccionario serializado."""
        return EstacionAmbiental.from_dict(data)
