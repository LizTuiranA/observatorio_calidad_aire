"""Menu CLI del modulo mediciones."""

from src.views.medicion_calidad_aire_view import MedicionCalidadAireView


def ejecutar_menu_medicion() -> None:
    """Abre el menu existente de mediciones."""
    MedicionCalidadAireView().mostrar_menu()
