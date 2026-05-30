"""Contexto simple de sesion para la GUI."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SesionActiva:
    """Representa el usuario y el rol actualmente autenticados."""

    usuario: str
    rol: str

    @property
    def puede_escribir(self) -> bool:
        """Indica si la sesion tiene permisos de escritura."""
        return self.rol == "empleado"