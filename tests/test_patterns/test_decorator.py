"""Pruebas del patron Decorator para notificaciones."""

from src.patterns.decorator.email_service import EmailService
from src.patterns.decorator.notificacion_decorator import NotificacionDecorator


def test_decorator_ejecuta_operacion_base():
    servicio = EmailService()
    respuesta = servicio.crear_o_actualizar_alerta("ALT001", "creada")

    assert respuesta == "Alerta ALT001 creada correctamente"


def test_decorator_envia_registra_notificacion_tras_actualizar(tmp_path):
    log_file = tmp_path / "notificaciones.log"
    servicio_decorado = NotificacionDecorator(EmailService(), log_file=log_file)

    respuesta = servicio_decorado.crear_o_actualizar_alerta("ALT002", "actualizada")

    assert respuesta == "Alerta ALT002 actualizada correctamente"
    contenido = log_file.read_text(encoding="utf-8")
    assert "Notificacion enviada para alerta ALT002 tras actualizada" in contenido
