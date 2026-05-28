"""Menu CLI del modulo alertas."""

from src.views.alerta_view import AlertaView


def ejecutar_menu_alerta() -> None:
    """Abre el menu existente de alertas."""
    AlertaView().mostrar_menu()
