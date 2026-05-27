"""Servicio de notificación por correo electrónico (Resend API).

Envía correos vía la API de Resend (https://resend.com) cuando hay una
API key configurada en variables de entorno. Si no la hay, opera en
modo simulación (imprime en consola) para no romper la ejecución ni
los tests.

Variables de entorno requeridas para envío real:
    RESEND_API_KEY   API Key de Resend (https://resend.com/api-keys)
    EMAIL_FROM       remitente (p. ej. onboarding@resend.dev sin dominio propio)
    EMAIL_TO         destinatario; debe ser el correo con el que te registraste
                     en Resend si no has verificado un dominio propio
"""

import os

import resend

from src.exceptions.custom_exceptions import EmailEnvioError


class EmailService:
    """Envía notificaciones por correo electrónico usando Resend."""

    def __init__(
        self,
        api_key: str | None = None,
        remitente: str | None = None,
        destinatario: str | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("RESEND_API_KEY")
        self.remitente = remitente or os.getenv("EMAIL_FROM")
        self.destinatario = destinatario or os.getenv("EMAIL_TO")

    def enviar_notificacion(self, accion: str, detalles: str, entidad: str) -> None:
        asunto = f"Operación de {accion} en {entidad}"

        if not self._configurado():
            print(f"\n[📧 EMAIL SERVICE — SIMULADO] Notificación enviada sin funcionamiento real, verificar credenciales")
            print(f"Asunto: {asunto}")
            print(f"Mensaje: {detalles}\n")
            return

        resend.api_key = self.api_key
        try:
            resend.Emails.send(
                {
                    "from": str(self.remitente),
                    "to": str(self.destinatario),
                    "subject": asunto,
                    "text": detalles,
                }
            )
        except Exception as e:
            raise EmailEnvioError(
                f"No se pudo enviar el correo a {self.destinatario}: {e}"
            ) from e
        print(f"\n[EMAIL SERVICE] Correo enviado a {self.destinatario}.")
        print(f"Asunto: {asunto}\n")

    def _configurado(self) -> bool:
        return all([self.api_key, self.remitente, self.destinatario])
