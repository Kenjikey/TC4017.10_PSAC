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