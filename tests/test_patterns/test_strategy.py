"""Pruebas del patron Strategy para clasificacion de PM2.5."""

from src.patterns.strategy.estrategia_clasificacion import (
    ClasificadorCalidadAire,
    EstrategiaAcademica,
    EstrategiaPreventiva,
)


def test_strategy_academica_clasifica_correctamente():
    clasificador = ClasificadorCalidadAire(EstrategiaAcademica())

    assert clasificador.clasificar(30) == "Medio"


def test_strategy_preventiva_es_mas_estricta():
    clasificador_preventivo = ClasificadorCalidadAire(EstrategiaPreventiva())
    clasificador_academico = ClasificadorCalidadAire(EstrategiaAcademica())

    assert clasificador_preventivo.clasificar(40) == "Alto"
    assert clasificador_academico.clasificar(40) == "Medio"
