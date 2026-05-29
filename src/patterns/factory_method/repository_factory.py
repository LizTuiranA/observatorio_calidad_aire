"""Factory Method para crear repositorios segun la entidad."""

from pathlib import Path

from src.repositories.alerta_repository import AlertaRepository


class RepositoryFactory:
    """Centraliza la creacion de repositorios del sistema."""

    @staticmethod
    def crear_repository(entidad: str, data_file: str | Path | None = None):
        """Crea un repositorio segun el nombre de la entidad."""
        entidad_normalizada = entidad.strip().lower()

        if entidad_normalizada == "alerta":
            return AlertaRepository(data_file=data_file)

        raise ValueError(f"Entidad no soportada: {entidad}")
