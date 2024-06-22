import subprocess

def sumar_array_ensamblador(array):
    input_data = ','.join(f"{x}" for x in array) + '\n'  # Convertir array a string
    result = subprocess.run(['./promedio'], input=input_data, text=True, capture_output=True)
    return result.returncode  # Convertir salida a entero

# Ejemplo de uso:
array = [12,45,2,8,81,7,63,7,1,2,7,96,5, 852, 45]
resultado = sumar_array_ensamblador(array)
print(f"El promedio es: {resultado}")


