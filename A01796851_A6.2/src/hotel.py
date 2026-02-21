"""
 Actividad 6.2. Ejercicio de programación 3: Sistema de Reservaciones
"""
import json
import os


class Hotel:
    """Clase para gestionar la información de los hoteles."""

    FILE_PATH = 'data/hotels.json'

    def __init__(self, hotel_id, name, location, rooms):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms = rooms
        # Inicializamos disponibilidad internamente
        self.a_rooms = rooms

    @classmethod
    def load_hotels(cls):
        """Carga los hoteles desde el archivo JSON."""
        if not os.path.exists(cls.FILE_PATH):
            return []
        try:
            with open(cls.FILE_PATH, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al cargar datos: {e}")
            return []

    @classmethod
    def save_hotels(cls, hotels):
        """Guarda la lista de hoteles en el archivo JSON."""
        try:
            with open(cls.FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump(hotels, file, indent=4)
        except IOError as e:
            print(f"Error al guardar datos: {e}")

    def reserve_room(self):
        """Método de instancia para reservar. Arregla el AttributeError."""
        if self.a_rooms > 0:
            self.a_rooms -= 1
            return True
        return False

    def cancel_reservation(self):
        """Método de instancia para cancelar. Arregla el AttributeError."""
        if self.a_rooms < self.rooms:
            self.a_rooms += 1
            return True
        return False

    @classmethod
    def create_hotel(cls, hotel_id, name, location, rooms):
        """Crea un nuevo hotel y lo persiste."""
        hotels = cls.load_hotels()
        # Verificar si ya existe el ID
        if any(h['hotel_id'] == hotel_id for h in hotels):
            print(f"Error: El hotel con ID {hotel_id} ya existe.")
            return

        hotels.append({
            'hotel_id': hotel_id,
            'name': name,
            'location': location,
            'rooms': rooms
        })
        cls.save_hotels(hotels)

    @classmethod
    def delete_hotel(cls, hotel_id):
        """Elimina un hotel por su ID."""
        hotels = cls.load_hotels()
        updated_hotels = [h for h in hotels if h['hotel_id'] != hotel_id]
        cls.save_hotels(updated_hotels)

    def display_info(self):
        """Muestra la información detallada del hotel en consola."""
        info = (f"ID: {self.hotel_id} | Hotel: {self.name} | "
                f"Ubicación: {self.location} | "
                f"Habitaciones: {self.rooms}")
        print(info)

    def modify_hotel(self, name=None, location=None, rooms=None):
        """Modifica los atributos del hotel y actualiza el archivo JSON."""
        if name:
            self.name = name
        if location:
            self.location = location
        if rooms:
            self.rooms = rooms

        # Después de modificar el objeto, actualizamos la base de datos
        hotels = self.load_hotels()
        for hotel in hotels:
            if hotel['hotel_id'] == self.hotel_id:
                hotel.update({
                    'name': self.name,
                    'location': self.location,
                    'rooms': self.rooms
                })
        self.save_hotels(hotels)
        print(f"Hotel {self.hotel_id} modificado exitosamente.")
