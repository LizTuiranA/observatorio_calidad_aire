"""Pruebas de persistencia JSON para estaciones ambientales."""

import json

import pytest

from src.exceptions.custom_exceptions import ArchivoInvalidoError, RegistroNoEncontradoError
from src.models.estacion_ambiental import DuplicateEstacionError, EstacionAmbiental
from src.repositories.estacion_repository import EstacionRepository


def _estacion_base(**overrides) -> EstacionAmbiental:
    datos = {
        "id_estacion": "EST-100",
        "nombre": "Centro",
        "municipio": "05001",
        "tipo_estacion": "Fija",
        "estado": "Activa",
    }
    datos.update(overrides)
    return EstacionAmbiental(**datos)


def test_repository_crea_y_lista_estaciones(tmp_path):
    repo = EstacionRepository(tmp_path / "estaciones.json")

    creada = repo.crear(_estacion_base())

    assert creada.id_estacion == "EST-100"
    assert repo.buscar("EST-100") is not None
    assert len(repo.listar()) == 1


def test_repository_rechaza_ids_duplicados(tmp_path):
    repo = EstacionRepository(tmp_path / "estaciones.json")
    repo.crear(_estacion_base())

    with pytest.raises(DuplicateEstacionError):
        repo.crear(_estacion_base(nombre="Otro nombre"))


def test_repository_buscar_inexistente_devuelve_none(tmp_path):
    repo = EstacionRepository(tmp_path / "estaciones.json")

    assert repo.buscar("EST-999") is None


def test_repository_lee_archivo_vacio_como_lista(tmp_path):
    archivo = tmp_path / "estaciones.json"
    archivo.write_text("", encoding="utf-8")

    repo = EstacionRepository(archivo)

    assert repo.listar() == []


def test_repository_rechaza_json_invalido_sin_lista(tmp_path):
    archivo = tmp_path / "estaciones.json"
    archivo.write_text(json.dumps({"id_estacion": "NO-LISTA"}), encoding="utf-8")

    repo = EstacionRepository(archivo)

    with pytest.raises(ArchivoInvalidoError):
        repo.listar()


def test_repository_actualiza_y_elimina(tmp_path):
    repo = EstacionRepository(tmp_path / "estaciones.json")
    repo.crear(_estacion_base())

    actualizada = repo.actualizar(
        _estacion_base(nombre="Centro Actualizado", estado="Inactiva")
    )

    assert actualizada.nombre == "Centro Actualizado"
    assert repo.buscar("EST-100").estado == "Inactiva"

    assert repo.eliminar("EST-100") is True
    assert repo.buscar("EST-100") is None


def test_repository_eliminar_inexistente_lanza_error(tmp_path):
    repo = EstacionRepository(tmp_path / "estaciones.json")

    with pytest.raises(RegistroNoEncontradoError):
        repo.eliminar("EST-999")
"""Pruebas unitarias para EstacionRepository y EstacionAmbiental."""

import pytest

from src.models.estacion_ambiental import DuplicateEstacionError, EstacionAmbiental, EstacionValidationError
from src.repositories.estacion_repository import EstacionRepository


def test_1_crear_estacion_valida(tmp_path):
    repo = EstacionRepository(tmp_path / "estaciones.json")
    estacion = EstacionAmbiental("EST001", "Estacion Centro", "Bogota", "Fija", "Activa")
    repo.crear(estacion)
    encontrada = repo.buscar("EST001")
    assert encontrada is not None
    assert encontrada.nombre == "Estacion Centro"


def test_2_rechazar_estacion_sin_id(tmp_path):
    _ = EstacionRepository(tmp_path / "estaciones.json")
    with pytest.raises(EstacionValidationError):
        EstacionAmbiental("", "Estacion Centro", "Bogota", "Fija", "Activa")


def test_3_rechazar_estacion_sin_nombre(tmp_path):
    _ = EstacionRepository(tmp_path / "estaciones.json")
    with pytest.raises(EstacionValidationError):
        EstacionAmbiental("EST001", "", "Bogota", "Fija", "Activa")


def test_4_rechazar_estacion_sin_municipio(tmp_path):
    _ = EstacionRepository(tmp_path / "estaciones.json")
    with pytest.raises(EstacionValidationError):
        EstacionAmbiental("EST001", "Estacion Centro", "", "Fija", "Activa")


def test_5_rechazar_estado_invalido(tmp_path):
    _ = EstacionRepository(tmp_path / "estaciones.json")
    with pytest.raises(EstacionValidationError):
        EstacionAmbiental("EST001", "Estacion Centro", "Bogota", "Fija", "Suspendida")


def test_6_rechazar_estacion_duplicada(tmp_path):
    repo = EstacionRepository(tmp_path / "estaciones.json")
    repo.crear(EstacionAmbiental("EST001", "Estacion Centro", "Bogota", "Fija", "Activa"))
    with pytest.raises(DuplicateEstacionError):
        repo.crear(EstacionAmbiental("EST001", "Estacion Norte", "Bogota", "Movil", "Activa"))


def test_7_listar_estaciones(tmp_path):
    repo = EstacionRepository(tmp_path / "estaciones.json")
    repo.crear(EstacionAmbiental("EST001", "Centro", "Bogota", "Fija", "Activa"))
    repo.crear(EstacionAmbiental("EST002", "Sur", "Bogota", "Movil", "Activa"))
    estaciones = repo.listar()
    assert len(estaciones) == 2


def test_8_buscar_estacion_existente(tmp_path):
    repo = EstacionRepository(tmp_path / "estaciones.json")
    repo.crear(EstacionAmbiental("EST001", "Centro", "Bogota", "Fija", "Activa"))
    encontrada = repo.buscar("EST001")
    assert encontrada is not None
    assert encontrada.id_estacion == "EST001"


def test_9_actualizar_estacion(tmp_path):
    repo = EstacionRepository(tmp_path / "estaciones.json")
    repo.crear(EstacionAmbiental("EST001", "Centro", "Bogota", "Fija", "Activa"))
    repo.actualizar(EstacionAmbiental("EST001", "Centro Modificada", "Bogota", "Fija", "Inactiva"))
    encontrada = repo.buscar("EST001")
    assert encontrada.nombre == "Centro Modificada"
    assert encontrada.estado == "Inactiva"


def test_10_eliminar_estacion(tmp_path):
    repo = EstacionRepository(tmp_path / "estaciones.json")
    repo.crear(EstacionAmbiental("EST001", "Centro", "Bogota", "Fija", "Activa"))
    repo.eliminar("EST001")
    assert repo.buscar("EST001") is None
