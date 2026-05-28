"""Pruebas del patron Factory Method para repositorios."""

import pytest

from src.patterns.factory_method.repository_factory import RepositoryFactory
from src.repositories.alerta_repository import AlertaRepository


def test_factory_method_crea_repository_alerta(tmp_path):
    repo = RepositoryFactory.crear_repository("alerta", data_file=tmp_path / "alertas.json")

    assert isinstance(repo, AlertaRepository)


def test_factory_method_error_entidad_no_soportada():
    with pytest.raises(ValueError, match="Entidad no soportada"):
        RepositoryFactory.crear_repository("sensor")
