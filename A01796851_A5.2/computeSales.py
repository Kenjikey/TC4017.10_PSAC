# pylint: disable=invalid-name
"""
Programa para calcular el costo total de ventas desde archivos JSON.
"""

import sys
import json
import time
import os


def load_json_file(file_path):
    """Carga un archivo JSON y maneja errores de lectura."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no fue encontrado.")
    except json.JSONDecodeError:
        print(f"Error: El archivo '{file_path}' no es un JSON válido.")
    return None


def compute_total_sales(price_catalogue, sales_record):
    """Calcula el total de ventas cruzando precios y registros."""
    total_cost = 0.0
    errors = []
    price_map = {}

    for item in price_catalogue:
        name = item.get("title")
        price = item.get("price")
        if name and isinstance(price, (int, float)):
            price_map[name] = price

    for record in sales_record:
        product_name = record.get("Product")
        quantity = record.get("Quantity")

        if product_name in price_map and isinstance(quantity, (int, float)):
            total_cost += price_map[product_name] * quantity
        else:
            msg = f"Dato inválido o no encontrado: {record}"
            errors.append(msg)

    return total_cost, errors


def format_save_results(total, elapsed_time, sales_file, errors):
    """Formatea los resultados, los imprime y los guarda."""
    for error in errors:
        print(f"Advertencia: {error}")

    header = "-" * 40
    result_output = (
        f"{header}\n"
        f"REPORTE DE VENTAS PARA: {sales_file}\n"
        f"{header}\n"
        f"Total de ventas calculadas: ${total:,.2f}\n"
        f"Tiempo de ejecución: {elapsed_time:.4f} segundos\n"
        f"{header}"
    )

    print(result_output)

    output_dir = "Results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Usamos el nombre limpio para el archivo de salida
    file_name = f"SalesResults_{sales_file}.txt"
    file_path = os.path.join(output_dir, file_name)

    try:
        with open(file_path, "w", encoding="utf-8") as out_file:
            out_file.write(result_output)
        print(f"Archivo guardado en: {file_path}")
    except IOError as e:
        print(f"Error al escribir en '{file_path}': {e}")


def main():
    """Función principal para obtener el cálculo de ventas."""
    usage_msg = "Uso: python computeSales.py catalogue.json sales.json"
    if len(sys.argv) != 3:
        print(usage_msg)
        return

    start_time = time.time()
    price_file = sys.argv[1]
    sales_arg = sys.argv[2]

    prices = load_json_file(price_file)
    sales_data = load_json_file(sales_arg)

    if prices is None or sales_data is None:
        return

    total_calculated, found_errors = compute_total_sales(prices, sales_data)
    elapsed = time.time() - start_time

    # Esto elimina las carpetas (Sales_list/) del nombre del resultado.
    clean_sales_name = os.path.basename(sales_arg)

    format_save_results(total_calculated, elapsed, clean_sales_name,
                        found_errors)


if __name__ == "__main__":
    main()
