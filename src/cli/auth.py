"""Autenticacion simple por consola para empleados."""

from dataclasses import dataclass
from getpass import getpass
import os


@dataclass(frozen=True)
class AuthConfig:
    """Configuracion de autenticacion para la CLI."""

    username: str
    password: str
    max_attempts: int = 3


class AuthService:
    """Autenticacion basica por consola usando variables de entorno o valores por defecto."""

    def __init__(
        self,
        username_env: str = "CLI_USER",
        password_env: str = "CLI_PASSWORD",
        default_username: str = "empleado",
        default_password: str = "empleado123",
        max_attempts: int = 3,
        input_func=input,
        password_func=getpass,
    ) -> None:
        self._config = AuthConfig(
            username=os.getenv(username_env, default_username),
            password=os.getenv(password_env, default_password),
            max_attempts=max_attempts,
        )
        self._input = input_func
        self._password = password_func

    def autenticar(self) -> bool:
        """Solicita credenciales hasta agotar intentos."""
        print("\n--- Acceso de empleados ---")
        for intento in range(1, self._config.max_attempts + 1):
            usuario = self._input("Usuario: ").strip()
            clave = self._password("Clave: ").strip()

            if usuario == self._config.username and clave == self._config.password:
                print("Acceso concedido.")
                return True

            print(
                f"Credenciales invalidas. Intento {intento}/{self._config.max_attempts}."
            )

        print("Acceso denegado.")
        return False
