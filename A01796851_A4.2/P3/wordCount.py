# pylint: disable=invalid-name
"""
Programa: wordCount.py
Descripción: Cuenta la frecuencia de palabras en un archivo de texto
             utilizando algoritmos básicos.
"""

import sys
import time
import os


def get_word_frequency(filename):
    """Lee el archivo y cuenta la frecuencia de cada palabra."""
    word_counts = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                # Separamos por espacios y limpiamos espacios en blanco
                words = line.split()
                for word in words:
                    # Limpiar puntuación y pasar a minúsculas
                    clean_word = word.strip().lower()
                    if clean_word:
                        # Algoritmo básico de conteo con diccionario
                        if clean_word in word_counts:
                            word_counts[clean_word] += 1
                        else:
                            word_counts[clean_word] = 1
    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no existe.")
        return None
    except Exception as error:  # pylint: disable=broad-except
        print(f"Error al procesar el archivo: {error}")
        return None
    return word_counts


def save_and_print_results(counts, filename, elapsed_time):
    """Formatea, imprime y guarda los resultados en el archivo."""
    # Extraer nombre para el archivo de salida
    base_name = os.path.splitext(os.path.basename(filename))[0]
    output_name = f"WordCountResults_{base_name}.txt"
    # Construcción del reporte
    lines = [
        "--- Conteo de Palabras ---",
        f"Archivo: {filename}",
        f"Tiempo de ejecución: {elapsed_time:.6f} segundos",
        f"{'Palabra':<20} | {'Frecuencia':<10}",
        "-" * 35
    ]

    # Añadir cada palabra y su frecuencia (ordenadas por frecuencia de mayor a menor)
    sorted_words = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    for word, freq in sorted_words:
        lines.append(f"{word:<20} | {freq:<10}")
    final_report = "\n".join(lines) + "\n"

    # Mostrar en consola y guardar
    print(final_report)
    with open(output_name, "a", encoding="utf-8") as out_file:
        out_file.write(final_report)


def main():
    """Función principal (Orquestador)."""
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Uso: python wordCount.py fileWithData.txt")
        return
    input_file = sys.argv[1]
    results = get_word_frequency(input_file)
    if results is not None:
        total_time = time.time() - start_time
        save_and_print_results(results, input_file, total_time)


if __name__ == "__main__":
    main()
