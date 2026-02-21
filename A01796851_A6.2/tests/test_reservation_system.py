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

# --- PRUEBAS DE EXCEPCIONES Y MANEJO DE ERRORES (REQ 5) ---

    def test_hotel_load_corrupt_json(self):
        """Prueba la excepción JSONDecodeError en Hoteles."""
        with open('data/hotels.json', 'w', encoding='utf-8') as file:
            file.write("{ 'invalid': json }")  # JSON mal formado

        # Debe atrapar el error y devolver lista vacía
        hotels = Hotel.load_hotels()
        self.assertEqual(hotels, [])

    def test_reserve_room_no_availability(self):
        """Prueba el escenario donde no hay habitaciones (a_rooms = 0)."""
        hotel = Hotel(hotel_id=99, name="Full Hotel", location="Loc", rooms=1)
        hotel.a_rooms = 0  # Forzamos disponibilidad cero
        success = hotel.reserve_room()
        self.assertFalse(success)

    def test_cancel_reservation_invalid_limit(self):
        """Prueba que no se puede cancelar más de las habitaciones totales."""
        hotel = Hotel(hotel_id=99, name="Empty Hotel", location="Loc", rooms=5)
        hotel.a_rooms = 5  # Ya está lleno
        success = hotel.cancel_reservation()
        self.assertFalse(success)

    def test_reservation_with_non_existent_customer(self):
        """Prueba crear reservación con un cliente que no existe."""
        Hotel.create_hotel(1, "Hotel A", "Ubic", 10)
        # Intentamos reservar con un Customer ID que no hemos creado
        success = Reservation.create_reservation(res_id=1,
                                                 cust_id=999,
                                                 hot_id=1)
        self.assertFalse(success)

    def test_reservation_with_non_existent_hotel(self):
        """Prueba crear reservación con un hotel que no existe."""
        Customer.create_customer(1, "Kenji", "k@mail.com")
        # Intentamos reservar con un Hotel ID que no existe
        success = Reservation.create_reservation(res_id=1,
                                                 cust_id=1,
                                                 hot_id=999)
        self.assertFalse(success)

    def test_delete_non_existent_customer(self):
        """Prueba borrar un cliente que no está en el sistema."""
        success = Customer.delete_customer(customer_id=999)
        self.assertFalse(success)

    def test_delete_non_existent_hotel(self):
        """Prueba borrar un hotel que no existe."""
        # Suponiendo que implementaste delete_hotel similar a delete_customer
        # Si no lo tienes, puedes omitir este o adaptarlo
        hotels = Hotel.load_hotels()
        count_before = len(hotels)
        Hotel.delete_hotel(hotel_id=999)
        self.assertEqual(len(Hotel.load_hotels()), count_before)

# 1. Cubriendo Customer.display_info (0%) y modify_info (0%)
    def test_customer_extra_methods(self):
        """Cubre los métodos de visualización y modificación de clientes."""
        Customer.create_customer(customer_id=2, name="Ana", email="ana@mail.com")
        cust = Customer(customer_id=2, name="Ana", email="ana@mail.com")
        cust.display_info()  # Ejecuta la línea de impresión
        cust.modify_info(name="Ana Maria")  # Ejecuta la lógica de modificación
        self.assertEqual(cust.name, "Ana Maria")

    # 2. Cubriendo Hotel.cancel_reservation (0%) y delete_hotel (0%)
    def test_hotel_extra_methods(self):
        """Cubre cancelación, eliminación y visualización de hoteles."""
        hotel_inst = Hotel(hotel_id=201, name="Hotel Test", location="Cancun", rooms=10)
        hotel_inst.display_info()  # Esto ya no dará error de 'self'
        hotel_inst.cancel_reservation()

        # Probar eliminación
        Hotel.delete_hotel(hotel_id=201)
        self.assertEqual(len(Hotel.load_hotels()), 0)

    # 3. Cubriendo Reservation.__init__ (0%) y cancel_reservation (0%)
    def test_reservation_lifecycle(self):
        """Cubre el ciclo de vida completo de una reservación."""
        # Necesitamos instanciarla directamente para cubrir el __init__
        res_obj = Reservation(reservation_id=999, customer_id=1, hotel_id=101)
        self.assertEqual(res_obj.reservation_id, 999)

        # Preparar datos para probar la cancelación real
        Hotel.create_hotel(hotel_id=101, name="Hotel A", location="Ubic", rooms=10)
        Customer.create_customer(customer_id=1, name="Kenji", email="kenji@mail.com")
        Reservation.create_reservation(res_id=555, cust_id=1, hot_id=101)

        # Ahora sí, cancelar reservación existente
        success = Reservation.cancel_reservation(res_id=555)
        self.assertTrue(success)

    # 4. Forzando excepciones en archivos (Sube el % de los load/save)
    def test_file_io_errors(self):
        """Simula errores de archivos para cubrir los bloques except."""
        # Escribir algo que no sea JSON para disparar JSONDecodeError
        with open('data/reservations.json', 'w', encoding='utf-8') as f:
            f.write("no_soy_un_json")

        res = Reservation.load_reservations()
        self.assertEqual(res, [])


if __name__ == '__main__':
    unittest.main()
