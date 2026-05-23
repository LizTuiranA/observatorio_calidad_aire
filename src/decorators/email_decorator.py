from abc import ABC, abstractmethod
from src.models.municipio import Municipio

# Interfaz Base del Controlador
class IMunicipioController(ABC):
    @abstractmethod
    def crear_municipio(self, codigo_dane: str, nombre: str, departamento: str, poblacion: int, area: float):
        pass

    @abstractmethod
    def actualizar_municipio(self, codigo_dane: str, nombre: str, departamento: str, poblacion: int, area: float):
        pass

# Servicio de Correo
class EmailService:
    @staticmethod
    def enviar_notificacion(asunto: str, mensaje: str):
        print(f"\n📧 [EmailService] {asunto}: {mensaje}\n")

# GoF Decorator
class EmailNotificationDecorator(IMunicipioController):
    def __init__(self, controlador_base: IMunicipioController):
        self._controlador_base = controlador_base

    def crear_municipio(self, codigo_dane: str, nombre: str, departamento: str, poblacion: int, area: float):
        resultado = self._controlador_base.crear_municipio(codigo_dane, nombre, departamento, poblacion, area)
        EmailService.enviar_notificacion(
            "Nuevo Registro", 
            f"Se ha registrado el municipio {nombre} ({codigo_dane})."
        )
        return resultado

    def actualizar_municipio(self, codigo_dane: str, nombre: str, departamento: str, poblacion: int, area: float):
        resultado = self._controlador_base.actualizar_municipio(codigo_dane, nombre, departamento, poblacion, area)
        EmailService.enviar_notificacion(
            "Actualización", 
            f"Se han modificado los datos del municipio {nombre} ({codigo_dane})."
        )
        return resultado
    