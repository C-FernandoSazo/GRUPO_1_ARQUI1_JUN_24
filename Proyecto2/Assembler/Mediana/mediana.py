import subprocess

def sumar_array_ensamblador(array):
    input_data = ','.join(f"{x}" for x in array) + '\n'  # Convertir array a string
    result = subprocess.run(['./medianaAssembly'], input=input_data, text=True, capture_output=True)
    return result.returncode  # Convertir salida a entero

# Ejemplo de uso:
array = [12,5,52,69,8,3,4,78,25,655,32,74,12,65,9,789]
resultado = sumar_array_ensamblador(array)
print(f"La media es: {resultado}")