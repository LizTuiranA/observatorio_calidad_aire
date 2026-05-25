"""Patron Command para operaciones de alertas."""

from abc import ABC, abstractmethod


class ComandoAlerta(ABC):
    """Contrato base para comandos de alerta."""

    @abstractmethod
    def ejecutar(self):
        """Ejecuta una accion sobre alertas."""


class CrearAlertaCommand(ComandoAlerta):
    """Comando concreto para crear una alerta en repositorio."""

    def __init__(self, alerta_repository, alerta):
        self._alerta_repository = alerta_repository
        self._alerta = alerta

    def ejecutar(self):
        return self._alerta_repository.crear_alerta(self._alerta)


class HistorialComandos:
    """Invocador que ejecuta comandos y guarda historial."""

    def __init__(self) -> None:
        self._historial: list[str] = []

    def ejecutar(self, comando: ComandoAlerta):
        resultado = comando.ejecutar()
        self._historial.append(comando.__class__.__name__)
        return resultado

    def obtener_historial(self) -> list[str]:
        return list(self._historial)
