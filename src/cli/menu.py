"""Menu principal CLI para empleados."""

from src.cli.auth import AuthService
from src.cli.menus.menu_alerta import ejecutar_menu_alerta
from src.cli.menus.menu_estacion import ejecutar_menu_estacion
from src.cli.menus.menu_medicion import ejecutar_menu_medicion
from src.cli.menus.menu_municipio import ejecutar_menu_municipio


def mostrar_menu_principal() -> None:
    """Imprime el menu principal de la CLI."""
    print("\n--- Observatorio de Calidad del Aire ---")
    print("1. Modulo Estaciones")
    print("2. Modulo Municipios")
    print("3. Modulo Mediciones")
    print("4. Modulo Alertas")
    print("5. Salir")


def main() -> None:
    """Inicia autenticacion y muestra el menu principal."""
    auth = AuthService()
    if not auth.autenticar():
        return

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            ejecutar_menu_estacion()
        elif opcion == "2":
            ejecutar_menu_municipio()
        elif opcion == "3":
            ejecutar_menu_medicion()
        elif opcion == "4":
            ejecutar_menu_alerta()
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opcion invalida. Intente de nuevo.")
