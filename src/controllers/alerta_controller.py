"""Controlador para operaciones de AlertaAmbiental."""

from src.models.alerta_ambiental import AlertaAmbiental
from src.patterns.builder.reporte_alerta_builder import ReporteAlerta, ReporteAlertaBuilder
from src.patterns.command.comandos_alerta import CrearAlertaCommand, HistorialComandos
from src.patterns.facade.alerta_facade import AlertaFacade
from src.patterns.strategy.estrategia_clasificacion import (
    ClasificadorCalidadAire,
    EstrategiaAcademica,
    EstrategiaClasificacion,
)
from src.repositories.alerta_repository import AlertaRepository


class _ClasificadorEstrategiaAdapter:
    """Adapta Strategy al contrato minimo que espera el Facade."""

    def __init__(self, estrategia: EstrategiaClasificacion) -> None:
        self._clasificador = ClasificadorCalidadAire(estrategia)

    def clasificar_valor(self, valor: float) -> str:
        return self._clasificador.clasificar(valor)


class AlertaController:
    """Coordina la logica entre main y el repositorio."""

    def __init__(
        self,
        repository=None,
        estrategia: EstrategiaClasificacion | None = None,
    ):
        self.repository = repository or AlertaRepository()
        self._estrategia = estrategia or EstrategiaAcademica()
        self._facade = AlertaFacade(
            alerta_repository=self.repository,
            clasificador=_ClasificadorEstrategiaAdapter(self._estrategia),
        )
        self._historial = HistorialComandos()

    def crear_alerta(
        self,
        id_alerta,
        id_medicion,
        nivel,
        descripcion,
        fecha,
        estado,
        valor_pm25: float | None = None,
    ):
        if valor_pm25 is not None:
            nivel = self._clasificar_nivel(valor_pm25)
        alerta = AlertaAmbiental(id_alerta, id_medicion, nivel, descripcion, fecha, estado)
        return self._historial.ejecutar(CrearAlertaCommand(self.repository, alerta))

    def registrar_alerta_critica(
        self,
        id_alerta: str,
        id_medicion: str,
        valor_pm25: float,
        descripcion: str,
        fecha: str,
        estado_inicial: str = "Activa",
    ) -> AlertaAmbiental:
        """Registra una alerta calculando su nivel desde Strategy y Facade."""
        return self._facade.registrar_evento_critico(
            id_alerta=id_alerta,
            id_medicion=id_medicion,
            valor=valor_pm25,
            descripcion=descripcion,
            fecha=fecha,
            estado_inicial=estado_inicial,
        )

    def generar_reporte_alerta(
        self,
        alerta: AlertaAmbiental,
        municipio: str = "",
        mediciones: list[dict] | None = None,
        recomendaciones: list[str] | None = None,
    ) -> ReporteAlerta:
        """Construye un reporte de alerta usando Builder."""
        builder = (
            ReporteAlertaBuilder()
            .con_id_alerta(alerta.id_alerta)
            .con_municipio(municipio)
            .con_nivel(alerta.nivel)
            .con_descripcion(alerta.descripcion)
        )
        for medicion in mediciones or []:
            builder.agregar_medicion(medicion)
        for recomendacion in recomendaciones or []:
            builder.agregar_recomendacion(recomendacion)
        return builder.construir()

    def obtener_historial_comandos(self) -> list[str]:
        return self._historial.obtener_historial()

    def _clasificar_nivel(self, valor_pm25: float) -> str:
        return self._facade.clasificador.clasificar_valor(valor_pm25)

    def listar_alertas(self):
        return self.repository.listar_alertas()

    def buscar_alerta(self, id_alerta):
        return self.repository.buscar_alerta_por_id(id_alerta)

    def actualizar_alerta(self, id_alerta, id_medicion, nivel, descripcion, fecha, estado):
        alerta = AlertaAmbiental(id_alerta, id_medicion, nivel, descripcion, fecha, estado)
        return self.repository.actualizar_alerta(id_alerta, alerta)

    def eliminar_alerta(self, id_alerta):
        return self.repository.eliminar_alerta(id_alerta)
