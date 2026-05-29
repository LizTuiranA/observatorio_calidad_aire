"""Punto de entrada principal de la CLI de empleados."""

from dotenv import load_dotenv

from src.cli.menu import main as cli_main


load_dotenv()


def main() -> None:
    """Ejecuta la interfaz de linea de comandos principal."""
    cli_main()


if __name__ == "__main__":
    main()