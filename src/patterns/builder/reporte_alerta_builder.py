"""Patron Builder aplicado a la construccion de reportes de alertas."""

from dataclasses import dataclass, field


@dataclass
class ReporteAlerta:
    """Representa un reporte consolidado de alerta ambiental."""

    id_alerta: str = ""
    municipio: str = ""
    nivel: str = ""
    descripcion: str = ""
    mediciones: list[dict] = field(default_factory=list)
    recomendaciones: list[str] = field(default_factory=list)


class ReporteAlertaBuilder:
    """Construye de forma gradual un ReporteAlerta."""

    NIVELES_VALIDOS = {"Bajo", "Medio", "Alto"}

    def __init__(self) -> None:
        self._reporte = ReporteAlerta()

    def con_id_alerta(self, id_alerta: str) -> "ReporteAlertaBuilder":
        self._reporte.id_alerta = (id_alerta or "").strip()
        return self

    def con_municipio(self, municipio: str) -> "ReporteAlertaBuilder":
        self._reporte.municipio = (municipio or "").strip()
        return self

    def con_nivel(self, nivel: str) -> "ReporteAlertaBuilder":
        nivel_limpio = (nivel or "").strip()
        if nivel_limpio not in self.NIVELES_VALIDOS:
            raise ValueError("Nivel invalido para construir reporte")
        self._reporte.nivel = nivel_limpio
        return self

    def con_descripcion(self, descripcion: str) -> "ReporteAlertaBuilder":
        self._reporte.descripcion = (descripcion or "").strip()
        return self

    def agregar_medicion(self, medicion: dict) -> "ReporteAlertaBuilder":
        self._reporte.mediciones.append(medicion)
        return self

    def agregar_recomendacion(self, recomendacion: str) -> "ReporteAlertaBuilder":
        self._reporte.recomendaciones.append(recomendacion)
        return self

    def construir(self) -> ReporteAlerta:
        if not self._reporte.nivel:
            raise ValueError("No se puede construir reporte sin nivel")
        return self._reporte
