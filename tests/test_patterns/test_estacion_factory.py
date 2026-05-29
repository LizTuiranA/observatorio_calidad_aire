"""Pruebas unitarias para la Factory Method de estaciones."""

from src.models.estacion_ambiental import EstacionAmbiental
from src.patterns.factory_method.estacion_factory import EstacionFactory


def test_factory_crea_estacion_ambiental():
    estacion = EstacionFactory.crear(
        " EST-001 ",
        " Centro ",
        " Medellin ",
        " Fija ",
        " Activa ",
    )

    assert isinstance(estacion, EstacionAmbiental)
    assert estacion.id_estacion == "EST-001"
    assert estacion.nombre == "Centro"
    assert estacion.estado == "Activa"
