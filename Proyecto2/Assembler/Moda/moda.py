import subprocess

def sumar_array_ensamblador(array):
    input_data = ','.join(f"{x}" for x in array) + '\n'  # Convertir array a string
    result = subprocess.run(['./modalAssembly'], input=input_data, text=True, capture_output=True)
    return result.returncode  # Convertir salida a entero

# Ejemplo de uso:
array = [256,1,2,256]
resultado = sumar_array_ensamblador(array)
print(f"La moda es: {resultado}")