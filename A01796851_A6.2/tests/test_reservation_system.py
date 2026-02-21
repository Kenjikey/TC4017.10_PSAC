"""Pruebas unitarias para el sistema de reservaciones."""

import unittest
import os
from src.hotel import Hotel
from src.customer import Customer
from src.reservations import Reservation


class TestReservationSystem(unittest.TestCase):
    """Casos de prueba para Hotel, Customer y Reservation."""

    def setUp(self):
        """Configura un estado limpio antes de cada prueba."""
        # Asegurar que la carpeta data existe
        if not os.path.exists('data'):
            os.makedirs('data')

        # Limpiar archivos de datos
        Hotel.save_hotels([])
        Customer.save_customers([])
        Reservation.save_reservations([])

    def test_hotel_creation_and_modification(self):
        """Prueba la creación y modificación de un hotel."""
        Hotel.create_hotel(hotel_id=101,
                           name="Test Hotel",
                           location="CDMX",
                           rooms=10)
        hotels = Hotel.load_hotels()
        self.assertEqual(len(hotels), 1)

        # Probar modificación
        hotel_inst = Hotel(hotel_id=101,
                           name="Test Hotel",
                           location="CDMX",
                           rooms=10)
        hotel_inst.modify_hotel(name="Hotel Modificado")
        self.assertEqual(Hotel.load_hotels()[0]['name'], "Hotel Modificado")

    def test_customer_crud(self):
        """Prueba las operaciones CRUD de clientes."""
        Customer.create_customer(1, "Kenji Ramirez", "kenji@example.com")
        customers = Customer.load_customers()
        self.assertEqual(len(customers), 1)

        # Eliminar cliente
        Customer.delete_customer(1)
        self.assertEqual(len(Customer.load_customers()), 0)

    def test_reservation_flow(self):
        """Prueba el flujo completo: Hotel + Cliente = Reservación."""
        # 1. Preparar datos
        Hotel.create_hotel(1, "Plaza", "Cancun", 1)
        Customer.create_customer(customer_id=1,
                                 name="Kenji Ramirez",
                                 email="kenji@example.com")

        # 2. Crear reservación exitosa
        success = Reservation.create_reservation(500, 1, 1)
        self.assertTrue(success)

        # 3. Verificar que bajó la disponibilidad del hotel
        hotels = Hotel.load_hotels()
        self.assertEqual(hotels[0]['a_rooms'], 0)

        # 4. Intentar reservar sin disponibilidad (debe fallar)
        fail_res = Reservation.create_reservation(501, 1, 1)
        self.assertFalse(fail_res)

    def test_invalid_data_handling(self):
        """Prueba el manejo de archivos corruptos (Req 5)."""
        # Escribir basura en el archivo JSON
        with open('data/hotels.json', 'w', encoding='utf-8') as file:
            file.write("ESTO NO ES UN JSON VALIDO")

        # El programa debe continuar y devolver lista vacía sin tronar
        hotels = Hotel.load_hotels()
        self.assertEqual(hotels, [])


if __name__ == '__main__':
    unittest.main()
