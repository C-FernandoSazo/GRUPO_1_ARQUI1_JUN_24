import subprocess

def sumar_array_ensamblador(array):
    input_data = ','.join(f"{x}" for x in array) + '\n'  # Convertir array a string
    result = subprocess.run(['./modalAssembly'], input=input_data, text=True, capture_output=True)
    return result.returncode  # Convertir salida a entero

# Ejemplo de uso:
array = [12,52,63,6,89,6,7,41,52,6,7,41,23,6,7,66,6]
resultado = sumar_array_ensamblador(array)
print(f"La moda es: {resultado}")