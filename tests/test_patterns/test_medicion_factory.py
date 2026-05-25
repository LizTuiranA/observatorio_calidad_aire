"""Pruebas unitarias para MedicionFactory y creadores de mediciones."""

from datetime import datetime

import pytest

from src.exceptions.custom_exceptions import DatoInvalidoError
from src.factories.medicion_creator import MedicionCreator
from src.factories.medicion_factory import MedicionFactory
from src.models.medicion_calidad_aire import MedicionCalidadAirePM


def _datos_base(**overrides) -> dict:
    datos = {
        "id": "M001",
        "codigo_dane_municipio": "05001",
        "id_estacion": "EST-MED-01",
        "fecha": datetime(2026, 5, 20, 10, 0),
        "diametro_aerodinamico": "PM10",
        "medicion": 42.5,
    }
    datos.update(overrides)
    return datos


def _dict_serializado(**overrides) -> dict:
    datos = _datos_base(**overrides)
    return {
        "id": datos["id"],
        "codigo_dane_municipio": datos["codigo_dane_municipio"],
        "id_estacion": datos["id_estacion"],
        "fecha": datos["fecha"].isoformat(),
        "tipo": "PM",
        "diametro_aerodinamico": datos["diametro_aerodinamico"],
        "medicion": datos["medicion"],
    }


def test_factory_crea_medicion_pm():
    medicion = MedicionFactory.crear("PM", **_datos_base())

    assert isinstance(medicion, MedicionCalidadAirePM)
    assert medicion.id == "M001"
    assert medicion.diametro_aerodinamico == "PM10"


def test_factory_desde_dict_con_tipo():
    data = _dict_serializado(medicion=55.0)
    medicion = MedicionFactory.desde_dict(data)

    assert isinstance(medicion, MedicionCalidadAirePM)
    assert medicion.medicion == 55.0


def test_factory_desde_dict_compatibilidad_sin_tipo():
    data = _dict_serializado()
    data.pop("tipo")

    medicion = MedicionFactory.desde_dict(data)

    assert isinstance(medicion, MedicionCalidadAirePM)
    assert medicion.id == "M001"


def test_factory_desde_dict_sin_tipo_ni_diametro_falla():
    data = _dict_serializado()
    data.pop("tipo")
    data.pop("diametro_aerodinamico")

    with pytest.raises(DatoInvalidoError):
        MedicionFactory.desde_dict(data)


def test_factory_resolver_tipo_desconocido_falla():
    with pytest.raises(DatoInvalidoError):
        MedicionFactory.resolver("OZONO")


def test_factory_registrar_nuevo_creator():
    class _CreatorDummy(MedicionCreator):
        def crear(self, **datos):
            return MedicionCalidadAirePM(**datos)

        def desde_dict(self, data: dict):
            return MedicionCalidadAirePM.from_dict(data)

    originales = dict(MedicionFactory._creators)
    try:
        MedicionFactory.registrar("PM_DUMMY", _CreatorDummy())
        medicion = MedicionFactory.crear("PM_DUMMY", **_datos_base(id="M999"))
        assert isinstance(medicion, MedicionCalidadAirePM)
        assert medicion.id == "M999"
        assert "PM_DUMMY" in MedicionFactory.tipos_disponibles()
    finally:
        # Restablece el registro original para no contaminar otras pruebas.
        MedicionFactory._creators = originales
