"""Pruebas del decorator de email para municipios."""

import unittest
from unittest.mock import MagicMock, patch

from src.decorators.email_decorator_municipio import EmailDecoratorMunicipio
from src.models.municipio import Municipio
from src.repositories.municipio_repository import MunicipioRepository
from src.services.email_service import EmailService


class TestEmailDecoratorMunicipio(unittest.TestCase):
    """Pruebas que validan el patrón Decorator en municipios."""

    def setUp(self):
        """Configura mocks para las pruebas."""
        self.mock_repository = MagicMock(spec=MunicipioRepository)
        self.mock_email_service = MagicMock(spec=EmailService)
        self.decorator = EmailDecoratorMunicipio(
            self.mock_repository, self.mock_email_service
        )

    def test_crear_municipio_envia_notificacion(self):
        """Verifica que crear municipio envía notificación de email."""
        municipio = Municipio(
            id_municipio="05001",
            nombre="Medellín",
            departamento="Antioquia",
            region="Andina",
            estado="Activo",
        )
        self.mock_repository.crear.return_value = municipio

        resultado = self.decorator.crear(municipio)

        self.assertEqual(resultado, municipio)
        self.mock_repository.crear.assert_called_once_with(municipio)
        self.mock_email_service.enviar_notificacion.assert_called_once_with(
            "creación",
            "Municipio 05001 (Medellín) registrado",
            entidad="Municipio",
        )

    def test_actualizar_municipio_envia_notificacion(self):
        """Verifica que actualizar municipio envía notificación de email."""
        municipio_actualizado = Municipio(
            id_municipio="05001",
            nombre="Medellín Actualizado",
            departamento="Antioquia",
            region="Andina",
            estado="Inactivo",
        )
        self.mock_repository.actualizar.return_value = municipio_actualizado

        resultado = self.decorator.actualizar("05001", municipio_actualizado)

        self.assertEqual(resultado, municipio_actualizado)
        self.mock_repository.actualizar.assert_called_once_with(
            "05001", municipio_actualizado
        )
        self.mock_email_service.enviar_notificacion.assert_called_once_with(
            "actualización",
            "Municipio 05001 (Medellín Actualizado) actualizado",
            entidad="Municipio",
        )

    def test_actualizar_municipio_no_encontrado_no_envia_notificacion(self):
        """Verifica que si no existe municipio, no se envía notificación."""
        municipio = Municipio(
            id_municipio="99999",
            nombre="Inexistente",
            departamento="Desconocido",
            region="Desconocida",
            estado="Activo",
        )
        self.mock_repository.actualizar.return_value = None

        resultado = self.decorator.actualizar("99999", municipio)

        self.assertIsNone(resultado)
        self.mock_email_service.enviar_notificacion.assert_not_called()

    def test_eliminar_municipio_envia_notificacion(self):
        """Verifica que eliminar municipio envía notificación de email."""
        self.mock_repository.eliminar.return_value = True

        resultado = self.decorator.eliminar("05001")

        self.assertTrue(resultado)
        self.mock_repository.eliminar.assert_called_once_with("05001")
        self.mock_email_service.enviar_notificacion.assert_called_once_with(
            "eliminación", "Municipio 05001 eliminado", entidad="Municipio"
        )

    def test_eliminar_municipio_fallido_no_envia_notificacion(self):
        """Verifica que si eliminación falla, no se envía notificación."""
        self.mock_repository.eliminar.return_value = False

        resultado = self.decorator.eliminar("99999")

        self.assertFalse(resultado)
        self.mock_email_service.enviar_notificacion.assert_not_called()

    def test_listar_municipios_solo_delega(self):
        """Verifica que listar solo delega sin enviar notificaciones."""
        municipios_esperados = [
            Municipio(
                id_municipio="05001",
                nombre="Medellín",
                departamento="Antioquia",
                region="Andina",
                estado="Activo",
            )
        ]
        self.mock_repository.listar.return_value = municipios_esperados

        resultado = self.decorator.listar()

        self.assertEqual(resultado, municipios_esperados)
        self.mock_repository.listar.assert_called_once()
        self.mock_email_service.enviar_notificacion.assert_not_called()

    def test_buscar_por_id_solo_delega(self):
        """Verifica que buscar solo delega sin enviar notificaciones."""
        municipio_esperado = Municipio(
            id_municipio="05001",
            nombre="Medellín",
            departamento="Antioquia",
            region="Andina",
            estado="Activo",
        )
        self.mock_repository.buscar_por_id.return_value = municipio_esperado

        resultado = self.decorator.buscar_por_id("05001")

        self.assertEqual(resultado, municipio_esperado)
        self.mock_repository.buscar_por_id.assert_called_once_with("05001")
        self.mock_email_service.enviar_notificacion.assert_not_called()


if __name__ == "__main__":
    unittest.main()
