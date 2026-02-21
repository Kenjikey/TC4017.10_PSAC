"""Módulo para la gestión de clientes en el sistema de reservaciones."""

import json
import os


class Customer:
    """Clase que representa a un cliente y maneja su persistencia."""

    FILE_PATH = 'data/customers.json'

    def __init__(self, customer_id, name, email):
        """Inicializa los atributos del cliente."""
        self.customer_id = customer_id
        self.name = name
        self.email = email

    @classmethod
    def load_customers(cls):
        """Carga la lista de clientes desde el archivo JSON."""
        if not os.path.exists(cls.FILE_PATH):
            return []
        try:
            with open(cls.FILE_PATH, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as error:
            print(f"Error al leer el archivo de clientes: {error}")
            return []

    @classmethod
    def save_customers(cls, customers):
        """Guarda la lista de clientes en el archivo JSON."""
        try:
            with open(cls.FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump(customers, file, indent=4)
        except IOError as error:
            print(f"Error al guardar el archivo de clientes: {error}")

    @classmethod
    def create_customer(cls, customer_id, name, email):
        """Crea un nuevo cliente y lo guarda en el archivo."""
        customers = cls.load_customers()
        if any(c['customer_id'] == customer_id for c in customers):
            print(f"Error: El cliente con ID {customer_id} ya existe.")
            return None

        new_customer_data = {
            'customer_id': customer_id,
            'name': name,
            'email': email
        }
        customers.append(new_customer_data)
        cls.save_customers(customers)
        print(f"Cliente '{name}' creado exitosamente.")
        return cls(customer_id, name, email)

    @classmethod
    def delete_customer(cls, customer_id):
        """Elimina un cliente del registro por su ID."""
        customers = cls.load_customers()
        updated_customers = [c for c in customers
                             if c['customer_id'] != customer_id]

        if len(customers) == len(updated_customers):
            print(f"Error: No se encontró al cliente con ID {customer_id}.")
            return False

        cls.save_customers(updated_customers)
        print(f"Cliente con ID {customer_id} eliminado.")
        return True

    def display_info(self):
        """Muestra la información del cliente actual."""
        print(f"Cliente ID: {self.customer_id} | Nombre: {self.name} | "
              f"Email: {self.email}")

    def modify_info(self, name=None, email=None):
        """Modifica la información del cliente y actualiza el archivo."""
        if name:
            self.name = name
        if email:
            self.email = email

        customers = self.load_customers()
        for cust in customers:
            if cust['customer_id'] == self.customer_id:
                cust['name'] = self.name
                cust['email'] = self.email
                break
        self.save_customers(customers)
        print(f"Información del cliente {self.customer_id} actualizada.")
