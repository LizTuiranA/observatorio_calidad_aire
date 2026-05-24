"""Patron Facade para registrar eventos criticos de alerta."""

from typing import Protocol

from src.models.alerta_ambiental import AlertaAmbiental
from src.repositories.alerta_repository import AlertaRepository


class Clasificador(Protocol):
    """Contrato minimo para clasificar riesgo en el facade."""

    def clasificar_valor(self, valor: float) -> str:
        """Retorna nivel de riesgo para el valor recibido."""


class _NotificadorDummy:
    """Notificador simple para no acoplar el facade al modulo A7."""

    def __init__(self) -> None:
        self.eventos: list[str] = []

    def enviar(self, mensaje: str) -> None:
        self.eventos.append(mensaje)


class AlertaFacade:
    """Orquesta validacion, persistencia y notificacion de eventos criticos."""

    def __init__(
        self,
        alerta_repository: AlertaRepository | None = None,
        clasificador: Clasificador | None = None,
        notificador=None,
    ) -> None:
        self.alerta_repository = alerta_repository or AlertaRepository()
        self.clasificador = clasificador
        self.notificador = notificador or _NotificadorDummy()

    def registrar_evento_critico(
        self,
        id_alerta: str,
        id_medicion: str,
        valor: float,
        descripcion: str,
        fecha: str,
        estado_inicial: str = "Activa",
    ) -> AlertaAmbiental:
        if self.clasificador is None:
            raise ValueError("Se requiere un clasificador de riesgo")

        nivel = self.clasificador.clasificar_valor(valor)
        if nivel not in {"Bajo", "Medio", "Alto"}:
            raise ValueError("Nivel invalido para crear alerta")

        alerta = AlertaAmbiental(id_alerta, id_medicion, nivel, descripcion, fecha, estado_inicial)
        creada = self.alerta_repository.crear_alerta(alerta)
        self.notificador.enviar(f"Alerta {creada.id_alerta} registrada con nivel {creada.nivel}")
        return creada
