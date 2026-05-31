from src.controllers.estacion_controller import EstacionController
from src.controllers.medicion_calidad_aire_controller import MedicionCalidadAireController
from src.controllers.municipio_controller import MunicipioController

def ejecutar_menu_visitante() -> None:
    """Ejecuta el ciclo del menú para visitantes (solo lectura)."""
    # Instanciamos los controladores
    est_ctrl = EstacionController()
    med_ctrl = MedicionCalidadAireController()
    mun_ctrl = MunicipioController()

    while True:
        print("\n--- Menú Visitante ---")
        print("1. Ver Estaciones")
        print("2. Ver Mediciones")
        print("3. Ver Municipios")
        print("4. Volver al inicio")
        
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- Lista de Estaciones ---")
            try:
                # Ajusta el método "listar" al que hayan definido tus compañeros
                estaciones = est_ctrl.listar() 
                for e in estaciones:
                    print(f"ID: {e.id_estacion} | Nombre: {e.nombre} | Estado: {e.estado}")
            except Exception as e:
                print(f"Error al cargar estaciones: {e}")

        elif opcion == "2":
            print("\n--- Lista de Mediciones ---")
            try:
                mediciones = med_ctrl.listar()
                for m in mediciones:
                    print(f"ID: {m.id_medicion} | Contaminante: {m.contaminante} | Valor: {m.valor}")
            except Exception as e:
                print(f"Error al cargar mediciones: {e}")
                
        elif opcion == "3":
            print("\n--- Lista de Municipios ---")
            try:
                municipios = mun_ctrl.listar_municipios()
                for m in municipios:
                    print(f"ID: {m.id_municipio} | Nombre: {m.nombre} | Región: {m.region}")
            except Exception as e:
                print(f"Error al cargar municipios: {e}")

        elif opcion == "4":
            print("Regresando al menú principal...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")