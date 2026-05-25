"""Strategy para clasificar nivel de calidad de aire."""

from abc import ABC, abstractmethod


class EstrategiaClasificacion(ABC):
    """Contrato para estrategias de clasificacion."""

    @abstractmethod
    def clasificar_pm25(self, valor_pm25: float) -> str:
        """Retorna categoria de riesgo segun el valor PM2.5."""


class EstrategiaAcademica(EstrategiaClasificacion):
    """Clasificacion estandar usada en ejemplos academicos."""

    def clasificar_pm25(self, valor_pm25: float) -> str:
        if valor_pm25 <= 25:
            return "Bajo"
        if valor_pm25 <= 50:
            return "Medio"
        return "Alto"


class EstrategiaPreventiva(EstrategiaClasificacion):
    """Clasificacion mas estricta para alertas tempranas."""

    def clasificar_pm25(self, valor_pm25: float) -> str:
        if valor_pm25 <= 15:
            return "Bajo"
        if valor_pm25 <= 35:
            return "Medio"
        return "Alto"


class ClasificadorCalidadAire:
    """Contexto que aplica una estrategia de clasificacion."""

    def __init__(self, estrategia: EstrategiaClasificacion) -> None:
        self._estrategia = estrategia

    def cambiar_estrategia(self, estrategia: EstrategiaClasificacion) -> None:
        self._estrategia = estrategia

    def clasificar(self, valor_pm25: float) -> str:
        return self._estrategia.clasificar_pm25(valor_pm25)
