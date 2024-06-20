import subprocess

def sumar_array_ensamblador(array):
    input_data = ','.join(f"{x}" for x in array) + '\n'  # Convertir array a string
    result = subprocess.run(['./maxAssembly'], input=input_data, text=True, capture_output=True)
    return result.returncode  # Convertir salida a entero

# Ejemplo de uso:
array = [45,85,6,9,41,23,5,74,11,45,23,98,1,2,3,77,5,9,6,4,89]
resultado = sumar_array_ensamblador(array)
print(f"El mayor es: {resultado}")