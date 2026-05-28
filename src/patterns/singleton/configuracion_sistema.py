"""Singleton para concentrar rutas de archivos JSON del sistema."""

from pathlib import Path


class ConfiguracionSistema:
    """Mantiene una unica instancia con configuraciones compartidas."""

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar_por_primera_vez()
        return cls._instancia

    def _inicializar_por_primera_vez(self) -> None:
        base_dir = Path(__file__).resolve().parents[3] / "data"
        self.ruta_alertas_json = base_dir / "alertas.json"
        self.ruta_estaciones_json = base_dir / "estaciones.json"
        self.ruta_mediciones_json = base_dir / "mediciones.json"
        self.ruta_municipios_json = base_dir / "municipios.json"
