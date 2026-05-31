from src.cli.auth import AuthService
from src.cli.menus.menu_alerta import ejecutar_menu_alerta
from src.cli.menus.menu_estacion import ejecutar_menu_estacion
from src.cli.menus.menu_medicion import ejecutar_menu_medicion
from src.cli.menus.menu_municipio import ejecutar_menu_municipio
from src.cli.menus.menu_visitante import ejecutar_menu_visitante

def mostrar_menu_empleado() -> None:
    print("\n--- Gestión de Empleados ---")
    print("1. Modulo Estaciones")
    print("2. Modulo Municipios")
    print("3. Modulo Mediciones")
    print("4. Modulo Alertas")
    print("5. Cerrar Sesión")

def loop_empleado() -> None:
    auth = AuthService()
    if not auth.autenticar():
        return

    while True:
        mostrar_menu_empleado()
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
            print("Cerrando sesión de empleado...")
            break
        else:
            print("Opcion invalida. Intente de nuevo.")

def main() -> None:
    """Punto de entrada de la consola. Rutea entre Visitante y Empleado."""
    while True:
        print("\n=== SISTEMA CLI: OBSERVATORIO DE CALIDAD DEL AIRE ===")
        print("1. Ingresar como Empleado (Requiere autenticación)")
        print("2. Ingresar como Visitante (Solo lectura)")
        print("3. Salir del sistema")
        
        seleccion = input("Seleccione su rol: ").strip()
        
        if seleccion == "1":
            loop_empleado()
        elif seleccion == "2":
            ejecutar_menu_visitante()
        elif seleccion == "3":
            print("Saliendo del sistema CLI...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()