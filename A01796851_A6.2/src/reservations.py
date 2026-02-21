"""Módulo para la gestión de reservaciones vinculando Hoteles y Clientes."""

import json
import os
try:
    from src.hotel import Hotel
    from src.customer import Customer
except ImportError:
    from hotel import Hotel
    from customer import Customer


class Reservation:
    """Clase que maneja la creación y cancelación de reservaciones."""

    FILE_PATH = 'data/reservations.json'

    def __init__(self, reservation_id, customer_id, hotel_id):
        """Inicializa una instancia de reservación."""
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    @classmethod
    def load_reservations(cls):
        """Carga las reservaciones desde el archivo JSON."""
        if not os.path.exists(cls.FILE_PATH):
            return []
        try:
            with open(cls.FILE_PATH, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as error:
            print(f"Error al leer reservaciones: {error}")
            return []

    @classmethod
    def save_reservations(cls, reservations):
        """Guarda la lista de reservaciones en el archivo JSON."""
        try:
            with open(cls.FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump(reservations, file, indent=4)
        except IOError as error:
            print(f"Error al guardar reservaciones: {error}")

    @classmethod
    def create_reservation(cls, res_id, cust_id, hot_id):
        """Crea una reservación validando cliente, hotel y disponibilidad."""
        # 1. Validar que el cliente exista
        customers = Customer.load_customers()
        if not any(c['customer_id'] == cust_id for c in customers):
            print(f"Error: El Cliente {cust_id} no existe.")
            return False

        # 2. Validar que el hotel exista
        hotels_data = Hotel.load_hotels()
        hotel_data = next((h for h in hotels_data if h['hotel_id'] == hot_id),
                          None)
        if not hotel_data:
            print(f"Error: El Hotel {hot_id} no existe.")
            return False

        # 3. Validar disponibilidad y actualizar hotel
        # Creamos una instancia temporal para usar su método reserve_room
        temp_hotel = Hotel(
            hotel_id=hotel_data['hotel_id'],
            name=hotel_data['name'],
            location=hotel_data['location'],
            rooms=hotel_data['rooms']
        )

        # Asignamos manualmente la disponibilidad guardada
        temp_hotel.a_rooms = hotel_data.get('a_rooms', hotel_data['rooms'])

        if temp_hotel.reserve_room():
            # Actualizar el dato en la lista y guardar
            hotel_data['a_rooms'] = temp_hotel.a_rooms
            Hotel.save_hotels(hotels_data)
            reservations = cls.load_reservations()
            reservations.append({
                'reservation_id': res_id,
                'customer_id': cust_id,
                'hotel_id': hot_id
            })
            cls.save_reservations(reservations)
            print(
                f"Reservación {res_id} creada exitosamente.")
            return True

        return False

    @classmethod
    def cancel_reservation(cls, res_id):
        """Cancela una reservación y libera la habitación en el hotel."""
        reservations = cls.load_reservations()
        res_to_cancel = next((r for r in reservations
                              if r['reservation_id'] == res_id),
                             None)

        if not res_to_cancel:
            print(f"Error: No se encontró la reservación {res_id}.")
            return False

        # 1. Liberar la habitación en el hotel correspondiente
        hotels_data = Hotel.load_hotels()
        hotel_data = next((h for h in hotels_data
                           if h['hotel_id'] == res_to_cancel['hotel_id']),
                          None)

        if hotel_data:
            temp_hotel = Hotel(
                hotel_data['hotel_id'],
                hotel_data['name'],
                hotel_data['location'],
                hotel_data['rooms'],
            )
            # La disponibilidad se asigna después, no en el constructor
            temp_hotel.a_rooms = hotel_data.get('a_rooms', hotel_data['rooms'])
            temp_hotel.cancel_reservation()

        # 2. Eliminar del archivo de reservaciones
        updated_res = [r for r in reservations
                       if r['reservation_id'] != res_id]
        cls.save_reservations(updated_res)
        print(f"Reservación {res_id} cancelada.")
        return True
