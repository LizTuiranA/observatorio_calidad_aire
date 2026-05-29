"""Pruebas del patron Singleton para configuracion del sistema."""

from pathlib import Path

from src.patterns.singleton.configuracion_sistema import ConfiguracionSistema


def test_singleton_retorna_misma_instancia_en_dos_llamadas():
    config_1 = ConfiguracionSistema()
    config_2 = ConfiguracionSistema()

    assert config_1 is config_2


def test_singleton_comparte_estado_de_rutas_json():
    config_1 = ConfiguracionSistema()
    config_2 = ConfiguracionSistema()

    nueva_ruta = Path("data") / "alertas_personalizadas.json"
    config_1.ruta_alertas_json = nueva_ruta

    assert config_2.ruta_alertas_json == nueva_ruta
