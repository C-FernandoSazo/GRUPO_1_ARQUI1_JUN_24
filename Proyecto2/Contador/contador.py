import subprocess

def counter(array):
    input_data = ','.join(f"{x}" for x in array) + '\n'  # Convertir array a string
    print(input_data)
    result = subprocess.run(['./contAssembly'], input=input_data, text=True, capture_output=True)
    return result.returncode  # Convertir salida a entero

# Ejemplo de uso:
array = [17,2,3,4,5,68,78,748,2,78,4,89,13,455,4,25,855]
resultado = counter(array)
print(f"Cantidad de numeros: {resultado}")
