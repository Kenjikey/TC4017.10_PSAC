import unittest
from src.hotel import Hotel

class TestHotel(unittest.TestCase):
    """Pruebas unitarias para la clase Hotel."""

    def setUp(self):
        """Configuración previa a cada prueba."""
        # Limpiar o crear datos de prueba temporales
        Hotel.save_hotels([])

    def test_create_hotel(self):
        """Verifica la creación exitosa de un hotel."""
        Hotel.create_hotel(1, "Hotel CDMX", "Centro", 50)
        hotels = Hotel.load_hotels()
        self.assertEqual(len(hotels), 1)
        self.assertEqual(hotels[0]['name'], "Hotel CDMX")

if __name__ == '__main__':
    unittest.main()