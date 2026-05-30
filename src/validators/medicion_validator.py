"""Chain of Responsibility para validacion de mediciones de calidad del aire."""

from datetime import datetime

from src.exceptions.custom_exceptions import DatoInvalidoError
from src.repositories.estacion_repository import EstacionRepository
from src.repositories.municipio_repository import MunicipioRepository


class MedicionValidator:
    """Cadena de validaciones de negocio para mediciones."""

    def __init__(self, estaciones: EstacionRepository, municipios: MunicipioRepository) -> None:
        self._estaciones = estaciones
        self._municipios = municipios

    def validar(self, id_estacion: str, codigo_dane_municipio: str, fecha: datetime) -> None:
        self._municipio_existe(codigo_dane_municipio)
        self._estacion_existe(id_estacion)
        self._estacion_activa(id_estacion)
        self._estacion_municipio(id_estacion, codigo_dane_municipio)
        self._fecha_no_futura(fecha)

    def _municipio_existe(self, codigo_dane_municipio: str) -> None:
        if self._municipios.buscar_por_id(codigo_dane_municipio) is None:
            raise DatoInvalidoError(
                f"Municipio con codigo DANE {codigo_dane_municipio!r} no existe."
            )

    def _estacion_existe(self, id_estacion: str) -> None:
        if self._estaciones.buscar(id_estacion) is None:
            raise DatoInvalidoError(
                f"Estacion {id_estacion!r} no existe. Registrela antes de crear mediciones."
            )

    def _estacion_activa(self, id_estacion: str) -> None:
        estacion = self._estaciones.buscar(id_estacion)
        if estacion is not None and estacion.estado != "Activa":
            raise DatoInvalidoError(
                f"La estacion {id_estacion!r} esta {estacion.estado!r}. "
                "Solo se pueden registrar mediciones en estaciones Activas."
            )

    def _estacion_municipio(self, id_estacion: str, codigo_dane_municipio: str) -> None:
        estacion = self._estaciones.buscar(id_estacion)
        if estacion is not None and estacion.municipio != codigo_dane_municipio:
            raise DatoInvalidoError(
                f"La estacion {id_estacion!r} pertenece al municipio "
                f"{estacion.municipio!r}, no a {codigo_dane_municipio!r}."
            )

    def _fecha_no_futura(self, fecha: datetime) -> None:
        if fecha > datetime.now():
            raise DatoInvalidoError(
                f"La fecha {fecha.isoformat()} es futura. "
                "No se pueden registrar mediciones de momentos que aun no han ocurrido."
            )
