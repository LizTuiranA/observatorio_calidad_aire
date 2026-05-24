"""Punto de entrada de la aplicacion (Actividad 7)."""

from src.controllers.alerta_controller import AlertaController
from src.exceptions.custom_exceptions import (
    DatoInvalidoError,
    RegistroDuplicadoError,
    RegistroNoEncontradoError,
)
from src.exceptions.municipio_exceptions import (
    DatosMunicipioInvalidosError,
    MunicipioNoEncontradoError,
    ReglaNegocioMunicipioError,
)
from src.views.municipio_view import MunicipioView


def _mostrar_menu_principal() -> None:
    print("\n--- Observatorio de Calidad del Aire ---")
    print("1. Modulo Alertas")
    print("2. Modulo Municipios")
    print("3. Salir")


def _mostrar_menu_alertas() -> None:
    print("\n--- Menu Alertas ---")
    print("1. Crear alerta")
    print("2. Listar alertas")
    print("3. Buscar alerta")
    print("4. Actualizar alerta")
    print("5. Eliminar alerta")
    print("6. Volver")


def _pedir_datos_alerta(id_alerta_predefinido: str | None = None) -> tuple[str, str, str, str, str, str]:
    id_alerta = id_alerta_predefinido if id_alerta_predefinido else input("ID alerta: ").strip()
    id_medicion = input("ID medicion: ").strip()
    nivel = input("Nivel (Bajo/Medio/Alto): ").strip()
    descripcion = input("Descripcion: ").strip()
    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    estado = input("Estado (Activa/Cerrada): ").strip()
    return id_alerta, id_medicion, nivel, descripcion, fecha, estado


def _ejecutar_modulo_alertas(controller: AlertaController) -> None:
    while True:
        _mostrar_menu_alertas()
        opcion = input("Seleccione una opcion: ").strip()

        try:
            if opcion == "1":
                alerta = controller.crear_alerta(*_pedir_datos_alerta())
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
                if alerta is None:
                    print("Alerta no encontrada.")
                else:
                    print(alerta.to_dict())
            elif opcion == "4":
                id_alerta = input("ID alerta a actualizar: ").strip()
                alerta = controller.actualizar_alerta(*_pedir_datos_alerta(id_alerta))
                print(f"Alerta actualizada: {alerta.id_alerta}")
            elif opcion == "5":
                id_alerta = input("ID alerta a eliminar: ").strip()
                controller.eliminar_alerta(id_alerta)
                print("Alerta eliminada correctamente.")
            elif opcion == "6":
                return
            else:
                print("Opcion invalida. Intente de nuevo.")
        except (DatoInvalidoError, RegistroDuplicadoError, RegistroNoEncontradoError) as error:
            print(f"Error: {error}")


def main() -> None:
    alerta_controller = AlertaController()
    municipio_view = MunicipioView()

    while True:
        _mostrar_menu_principal()
        opcion = input("Seleccione una opcion: ").strip()

        try:
            if opcion == "1":
                _ejecutar_modulo_alertas(alerta_controller)
            elif opcion == "2":
                municipio_view.mostrar_menu()
            elif opcion == "3":
                print("Saliendo del sistema...")
                break
            else:
                print("Opcion invalida. Intente de nuevo.")
        except (
            DatoInvalidoError,
            RegistroDuplicadoError,
            RegistroNoEncontradoError,
            DatosMunicipioInvalidosError,
            MunicipioNoEncontradoError,
            ReglaNegocioMunicipioError,
        ) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
