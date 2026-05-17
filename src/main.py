"""Punto de entrada con menu de consola para AlertasAmbientales."""

from src.controllers.alerta_controller import AlertaController
from src.exceptions.custom_exceptions import (
    DatoInvalidoError,
    RegistroDuplicadoError,
    RegistroNoEncontradoError,
)


def mostrar_menu():
    print("\n--- Observatorio de Calidad del Aire ---")
    print("1. Crear alerta")
    print("2. Listar alertas")
    print("3. Buscar alerta")
    print("4. Actualizar alerta")
    print("5. Eliminar alerta")
    print("6. Salir")


def pedir_datos_alerta(id_alerta_predefinido=None):
    id_alerta = id_alerta_predefinido if id_alerta_predefinido else input("ID alerta: ")
    id_medicion = input("ID medicion: ")
    nivel = input("Nivel (Bajo/Medio/Alto): ")
    descripcion = input("Descripcion: ")
    fecha = input("Fecha (YYYY-MM-DD): ")
    estado = input("Estado (Activa/Cerrada): ")
    return id_alerta, id_medicion, nivel, descripcion, fecha, estado


def main():
    controller = AlertaController()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ").strip()

        try:
            if opcion == "1":
                datos = pedir_datos_alerta()
                alerta = controller.crear_alerta(*datos)
                print(f"Alerta creada: {alerta.id_alerta}")

            elif opcion == "2":
                alertas = controller.listar_alertas()
                if not alertas:
                    print("No hay alertas registradas.")
                for alerta in alertas:
                    print(alerta.to_dict())

            elif opcion == "3":
                id_alerta = input("ID alerta a buscar: ").strip()
                alerta = controller.buscar_alerta(id_alerta)
                if alerta:
                    print(alerta.to_dict())
                else:
                    print("Alerta no encontrada.")

            elif opcion == "4":
                id_alerta = input("ID alerta a actualizar: ").strip()
                datos = pedir_datos_alerta(id_alerta_predefinido=id_alerta)
                alerta = controller.actualizar_alerta(*datos)
                print(f"Alerta actualizada: {alerta.id_alerta}")

            elif opcion == "5":
                id_alerta = input("ID alerta a eliminar: ").strip()
                controller.eliminar_alerta(id_alerta)
                print("Alerta eliminada correctamente.")

            elif opcion == "6":
                print("Saliendo del sistema...")
                break

            else:
                print("Opcion invalida. Intente de nuevo.")

        except (DatoInvalidoError, RegistroDuplicadoError, RegistroNoEncontradoError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
