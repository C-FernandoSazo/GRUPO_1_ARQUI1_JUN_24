import subprocess

def counter_air(array):
    input_data = ','.join(f"{x}" for x in array) + '\n'  # Convertir array a string
    print(input_data)
    result = subprocess.run(['./airAssembly'], input=input_data, text=True, capture_output=True)
    result2 = subprocess.run(['./airbadAssembly'], input=input_data, text=True, capture_output=True)
    return result.returncode, result2.returncode  # Convertir salida a entero

# Ejemplo de uso:
array = [17,2,3,4,5,68,78,74,2,78,4,89,13,45,4,25,85]
resultado, resultado2 = counter_air(array)
print(f"La cantidad buena del aire es: {resultado}")
print(f"La cantidad mala del aire es: {resultado2}")
