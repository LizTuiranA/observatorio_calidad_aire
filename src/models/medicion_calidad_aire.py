"""Modelo de mediciones de calidad del aire (Res. 2254 de 2017).

Define la entidad base abstracta `MedicionCalidadAire` y una subclase
concreta por contaminante criterio. Cada subclase aporta sus propios
puntos de corte ICA; la base se encarga de la validacion comun y de
clasificar el nivel a partir del valor medido.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from src.exceptions.custom_exceptions import DatoInvalidoError


@dataclass(frozen=True, kw_only=True)
class MedicionCalidadAire(ABC):
    """Lectura de un contaminante tomada en una estacion."""

    # Origen del dato
    MANUAL: ClassVar[str] = "MANUAL"
    AUTO: ClassVar[str] = "AUTOMATICO"
    ORIGENES_VALIDOS: ClassVar[tuple] = (MANUAL, AUTO)

    # Categorias ICA (Res. 2254/2017, Tabla 6).
    BUENA: ClassVar[str] = "Buena"
    ACEPTABLE: ClassVar[str] = "Aceptable"
    DANINA_SENSIBLES: ClassVar[str] = "Daniña a la salud de grupos sensibles"
    DANINA: ClassVar[str] = "Daniña a la salud"
    MUY_DANINA: ClassVar[str] = "Muy daniña a la salud"
    PELIGROSA: ClassVar[str] = "Peligrosa"

    # Identificador del contaminante (lo sobrescribe cada subclase).
    TIPO: ClassVar[str] = ""

    id: str
    codigo_dane_municipio: str
    id_estacion: str
    fecha: datetime
    medicion: float
    origen: str = AUTO

    def __post_init__(self) -> None:
        if not self.id:
            raise DatoInvalidoError("id no puede estar vacio")
        if not self.codigo_dane_municipio:
            raise DatoInvalidoError("codigo_dane_municipio no puede estar vacio")
        if not self.id_estacion:
            raise DatoInvalidoError("id_estacion no puede estar vacio")
        if not isinstance(self.fecha, datetime):
            raise DatoInvalidoError("fecha debe ser datetime")
        if not isinstance(self.medicion, (int, float)):
            raise DatoInvalidoError("medicion debe ser numerica")
        if self.medicion <= 0:
            raise DatoInvalidoError("medicion debe ser positiva")
        if self.origen not in self.ORIGENES_VALIDOS:
            raise DatoInvalidoError(
                f"Origen invalido: {self.origen}. "
                f"Validos: {self.ORIGENES_VALIDOS}"
            )

    @property
    @abstractmethod
    def _puntos_corte(self) -> list[tuple[float, str]]:
        """Lista ordenada de (limite_superior, categoria_ICA)."""

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> "MedicionCalidadAire":
        """Reconstruye una instancia desde su forma serializada."""

    @property
    def nivel(self) -> str:
        """Categoria ICA correspondiente al valor medido."""
        for limite, categoria in self._puntos_corte:
            if self.medicion <= limite:
                return categoria
        return self.PELIGROSA

    def es_eliminable(self) -> bool:
        """Las mediciones automaticas son inmutables; solo se borran las manuales."""
        return self.origen == self.MANUAL

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "codigo_dane_municipio": self.codigo_dane_municipio,
            "id_estacion": self.id_estacion,
            "fecha": self.fecha.isoformat(),
            "tipo": type(self).TIPO,
            "medicion": self.medicion,
            "nivel": self.nivel,
            "origen": self.origen,
        }


@dataclass(frozen=True, kw_only=True)
class MedicionCalidadAirePM(MedicionCalidadAire):
    """Material particulado PM10 y PM2.5 (promedio 24h)."""

    TIPO: ClassVar[str] = "PM"
    PM10: ClassVar[str] = "PM10"
    PM25: ClassVar[str] = "PM2.5"
    DIAMETROS_VALIDOS: ClassVar[tuple] = (PM10, PM25)

    # Puntos de corte ICA por diametro (Res. 2254/2017, Tabla 6, µg/m³).
    _PUNTOS_CORTE: ClassVar[dict] = {
        PM10: [
            (54, MedicionCalidadAire.BUENA),
            (154, MedicionCalidadAire.ACEPTABLE),
            (254, MedicionCalidadAire.DANINA_SENSIBLES),
            (354, MedicionCalidadAire.DANINA),
            (424, MedicionCalidadAire.MUY_DANINA),
            (604, MedicionCalidadAire.PELIGROSA),
        ],
        PM25: [
            (12, MedicionCalidadAire.BUENA),
            (37, MedicionCalidadAire.ACEPTABLE),
            (55, MedicionCalidadAire.DANINA_SENSIBLES),
            (150, MedicionCalidadAire.DANINA),
            (250, MedicionCalidadAire.MUY_DANINA),
            (500, MedicionCalidadAire.PELIGROSA),
        ],
    }

    diametro_aerodinamico: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.diametro_aerodinamico not in self.DIAMETROS_VALIDOS:
            raise DatoInvalidoError(
                f"Diametro aerodinamico invalido: {self.diametro_aerodinamico}. "
                f"Validos: {self.DIAMETROS_VALIDOS}"
            )

    @property
    def _puntos_corte(self) -> list[tuple[float, str]]:
        return self._PUNTOS_CORTE[self.diametro_aerodinamico]

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["diametro_aerodinamico"] = self.diametro_aerodinamico
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "MedicionCalidadAirePM":
        return cls(
            id=data["id"],
            codigo_dane_municipio=data["codigo_dane_municipio"],
            id_estacion=data["id_estacion"],
            fecha=datetime.fromisoformat(data["fecha"]),
            diametro_aerodinamico=data["diametro_aerodinamico"],
            medicion=float(data["medicion"]),
            origen=data.get("origen", cls.AUTO),
        )
