import pytest

from src.controllers.alerta_controller import AlertaController


@pytest.fixture()
def repo_tmp(tmp_path):
    return tmp_path / "alertas_controller.json"


def test_crear_alerta_con_valor_usa_strategy_y_command(repo_tmp):
    controller = AlertaController(repository=None)
    controller.repository.data_file = repo_tmp
    controller.repository._asegurar_archivo()

    alerta = controller.crear_alerta(
        id_alerta="ALT-700",
        id_medicion="MED-700",
        nivel="Bajo",
        descripcion="Prueba de estrategia",
        fecha="2026-05-30",
        estado="Activa",
        valor_pm25=60,
    )

    assert alerta.nivel == "Alto"
    assert controller.obtener_historial_comandos() == ["CrearAlertaCommand"]
    assert controller.repository.buscar_alerta_por_id("ALT-700") is not None


def test_registrar_alerta_critica_y_generar_reporte(repo_tmp):
    controller = AlertaController(repository=None)
    controller.repository.data_file = repo_tmp
    controller.repository._asegurar_archivo()

    alerta = controller.registrar_alerta_critica(
        id_alerta="ALT-701",
        id_medicion="MED-701",
        valor_pm25=40,
        descripcion="Evento critico",
        fecha="2026-05-30",
    )

    reporte = controller.generar_reporte_alerta(
        alerta,
        municipio="Bogota",
        mediciones=[{"pm25": 40}],
        recomendaciones=["Reducir actividad al aire libre"],
    )

    assert alerta.nivel == "Medio"
    assert reporte.id_alerta == "ALT-701"
    assert reporte.municipio == "Bogota"
    assert reporte.mediciones == [{"pm25": 40}]
    assert reporte.recomendaciones == ["Reducir actividad al aire libre"]
