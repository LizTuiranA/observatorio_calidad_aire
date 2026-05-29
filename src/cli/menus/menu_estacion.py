"""Menu CLI del modulo estaciones."""

from src.views.estacion_view import EstacionView


def ejecutar_menu_estacion() -> None:
    """Abre el menu existente de estaciones."""
    EstacionView().mostrar_menu()
