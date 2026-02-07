# pylint: disable=invalid-name
"""
Programa: computeStatistics.py
Descripción: Calcula estadísticas descriptivas (Media, Mediana, Moda,
             Desviación Estándar y Varianza) a partir de un archivo.
"""

import sys
import time

def calculate_mean(data):
    """Calcula la media aritmética."""
    return sum(data) / len(data)


def calculate_median(data):
    """Calcula la mediana de una lista de números."""
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return sorted_data[mid]


def calculate_mode(data):
    """Calcula la moda (el valor que más se repite)."""
    frequency = {}
    for item in data:
        frequency[item] = frequency.get(item, 0) + 1
    max_freq = max(frequency.values())
    modes = [k for k, v in frequency.items() if v == max_freq]
    # Si todos se repiten igual, no hay una moda única
    if len(modes) == len(data):
        return "N/A"
    return modes[0] if len(modes) == 1 else modes


def calculate_variance(data, mean):
    """Calcula la varianza poblacional."""
    sum_sq_diff = sum((x - mean) ** 2 for x in data)
    return sum_sq_diff / len(data)


def main():
    """Función principal para ejecutar el programa."""
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Uso: python computeStatistics.py fileWithData.txt")
        return

    filename = sys.argv[1]
    numbers = []

    # Req 3: Manejo de datos inválidos
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                clean_line = line.strip()
                if clean_line:
                    try:
                        numbers.append(float(clean_line))
                    except ValueError:
                        print(f"Error: '{clean_line}' no es un número válido.")
    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no existe.")
        return

    if not numbers:
        print("Error: No se encontraron datos numéricos para procesar.")
        return

    # Req 2: Cálculos con algoritmos básicos
    mean = calculate_mean(numbers)
    median = calculate_median(numbers)
    mode = calculate_mode(numbers)
    variance = calculate_variance(numbers, mean)
    std_dev = variance ** 0.5  # Raíz cuadrada manual

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Formatear resultados
    results = (
        f"--- Estadísticas --- \n"
        f"Archivo: {filename}\n"
        f"Cantidad de elementos: {len(numbers)}\n"
        f"Media: {mean}\n"
        f"Mediana: {median}\n"
        f"Moda: {mode}\n"
        f"Varianza Poblacional: {variance}\n"
        f"Desv Estandar Poblacional: {std_dev}\n"
        f"Tiempo de ejecución: {elapsed_time:.6f} segundos\n"
        f"-------------------- \n"
    )

    # Req 2 y 7: Imprimir en pantalla y guardar en archivo
    print(results, filename)
    with open(f"StatisticsResults_{filename}.txt", "a", encoding="utf-8") as out_file:
        out_file.write(results + "\n")


if __name__ == "__main__":
    main()
