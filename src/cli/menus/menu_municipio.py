"""Menu CLI del modulo municipios."""

from src.views.municipio_view import MunicipioView


def ejecutar_menu_municipio() -> None:
    """Abre el menu existente de municipios."""
    MunicipioView().mostrar_menu()
