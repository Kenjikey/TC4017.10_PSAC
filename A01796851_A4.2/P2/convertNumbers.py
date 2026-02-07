# pylint: disable=invalid-name
"""
Programa: convertNumbers.py
Descripción: Convierte números a binario y hexadecimal.
"""

import sys
import time
import os


def to_binary(n):
    """Algoritmo manual para binario."""
    if n == 0:
        return "0"
    binary = ""
    is_neg = n < 0
    num = abs(int(n))
    while num > 0:
        binary = str(num % 2) + binary
        num //= 2
    return f"-{binary}" if is_neg else binary


def to_hexadecimal(n):
    """Algoritmo manual para hexadecimal."""
    if n == 0:
        return "0"
    chars = "0123456789ABCDEF"
    hexa = ""
    is_neg = n < 0
    num = abs(int(n))
    while num > 0:
        hexa = chars[num % 16] + hexa
        num //= 16
    return f"-{hexa}" if is_neg else hexa


def process_file(filename):
    """Lee el archivo y convierte los datos, manejando errores."""
    data_converted = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                clean = line.strip()
                if clean:
                    try:
                        num = int(float(clean))
                        data_converted.append((num, to_binary(num), to_hexadecimal(num)))
                    except ValueError:
                        print(f"Error: '{clean}' no es un número válido.")
    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no existe.")
        return None
    return data_converted


def save_results(results, filename, elapsed):
    """Genera el reporte y lo guarda en disco."""
    base = os.path.splitext(os.path.basename(filename))[0]
    out_name = f"ConvertionResults_{base}.txt"
    header = (
        f"--- Resultados ---\n"
        f"Archivo: {filename}\n"
        f"Tiempo: {elapsed:.6f} s\n"
        f"{'Num':>10} | {'Bin':>20} | {'Hex':>10}\n"
        + "-" * 50 + "\n"
    )
    body = "\n".join([f"{n:>10} | {b:>20} | {h:>10}" for n, b, h in results])
    final_text = header + body + "\n"
    print(final_text)
    with open(out_name, "a", encoding="utf-8") as f_out:
        f_out.write(final_text)


def main():
    """Orquestador principal."""
    start = time.time()
    if len(sys.argv) != 2:
        print("Uso: python convertNumbers.py file.txt")
        return

    fname = sys.argv[1]
    results = process_file(fname)
    if results is not None:
        elapsed = time.time() - start
        save_results(results, fname, elapsed)

if __name__ == "__main__":
    main()
    