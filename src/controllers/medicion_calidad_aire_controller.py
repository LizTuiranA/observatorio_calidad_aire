"""Controlador de mediciones (capa C del patron MVC).

Coordina la vista y el repositorio para implementar los casos de uso:
crear/actualizar/eliminar mediciones manuales y listarlas.
"""

from dataclasses import replace
from datetime import datetime
from typing import Optional

from src.exceptions.custom_exceptions import (
    DatoInvalidoError,
    RegistroDuplicadoError,
    RegistroNoEncontradoError,
)
from src.factories.medicion_factory import MedicionFactory
from src.models.medicion_calidad_aire import MedicionCalidadAire
from src.decorators.email_decorator_medicion import EmailDecoratorMedicion
from src.repositories.estacion_repository import EstacionRepository
from src.repositories.medicion_calidad_aire_repository import (
    IMedicionRepository,
    MedicionRepository,
    _canonical_id,
)
from src.services.email_service import EmailService
from src.views.medicion_calidad_aire_view import MedicionCalidadAireView


class MedicionController:
    """Orquesta los casos de uso del modulo de mediciones."""

    def __init__(
        self,
        repository: Optional[IMedicionRepository] = None,
        view: Optional[MedicionCalidadAireView] = None,
        estacion_repository: Optional[EstacionRepository] = None,
    ) -> None:
        self.repository = repository or EmailDecoratorMedicion(
            MedicionRepository(), EmailService()
        )
        self.view = view
        self._estaciones = estacion_repository or EstacionRepository()

    def crear_medicion(
        self,
        tipo: str,
        id: str,
        codigo_dane_municipio: str,
        id_estacion: str,
        fecha: datetime,
        medicion: float,
        **extra,
    ) -> None:
        """Registra una medicion MANUAL ingresada por el usuario."""
        id = _canonical_id(id)
        codigo_dane_municipio = _canonical_id(codigo_dane_municipio)
        id_estacion = _canonical_id(id_estacion)
        if self._estaciones.buscar(id_estacion) is None:
            self.view.show_error(
                f"Estacion {id_estacion!r} no existe. "
                "Registrela antes de crear mediciones manuales."
            )
            return
        try:
            nueva = MedicionFactory.crear(
                tipo,
                id=id,
                codigo_dane_municipio=codigo_dane_municipio,
                id_estacion=id_estacion,
                fecha=fecha,
                medicion=medicion,
                origen=MedicionCalidadAire.MANUAL,
                **extra,
            )
            self.repository.crear_medicion(nueva)
        except (DatoInvalidoError, RegistroDuplicadoError) as e:
            self.view.show_error(str(e))
            return
        self.view.show_message(
            f"Medicion {id} creada manualmente — nivel: {nueva.nivel}"
        )

    def actualizar_medicion(
        self,
        medicion_id: str,
        codigo_dane_municipio: Optional[str] = None,
        id_estacion: Optional[str] = None,
        fecha: Optional[datetime] = None,
        medicion: Optional[float] = None,
        **extra,
    ) -> None:
        """Modifica una medicion MANUAL existente (las AUTO son inmutables)."""
        existente = self._buscar_editable(_canonical_id(medicion_id))
        if existente is None:
            return

        cambios = {}
        if codigo_dane_municipio is not None:
            cambios["codigo_dane_municipio"] = _canonical_id(codigo_dane_municipio)
        if id_estacion is not None:
            cambios["id_estacion"] = _canonical_id(id_estacion)
        if fecha is not None:
            cambios["fecha"] = fecha
        if medicion is not None:
            cambios["medicion"] = medicion
        cambios.update(extra)

        try:
            actualizada = replace(existente, **cambios)
            self.repository.actualizar_medicion(actualizada)
        except (DatoInvalidoError, RegistroNoEncontradoError) as e:
            self.view.show_error(str(e))
            return

        self.view.show_message(
            f"Medicion {existente.id} actualizada — nivel: {actualizada.nivel}"
        )

    def _buscar_editable(self, medicion_id: str) -> Optional[MedicionCalidadAire]:
        """Devuelve la medicion si existe y es editable; muestra error y devuelve None si no."""
        existente = self.repository.buscar_medicion_por_id(medicion_id)
        if existente is None:
            self.view.show_error(f"No existe medicion con id {medicion_id}")
            return None
        if existente.origen == MedicionCalidadAire.AUTO:
            self.view.show_error(
                "Las mediciones automaticas son inmutables. "
                "Solo se pueden editar mediciones MANUALES."
            )
            return None
        return existente

    def eliminar_medicion(self, medicion_id: str) -> None:
        medicion_id = _canonical_id(medicion_id)
        try:
            self.repository.eliminar_medicion(medicion_id)
        except (DatoInvalidoError, RegistroNoEncontradoError) as e:
            self.view.show_error(str(e))
            return
        self.view.show_message(f"Medicion {medicion_id} eliminada")

    def listar_mediciones(self) -> None:
        self.view.show_mediciones(self.repository.listar_mediciones())
