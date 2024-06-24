import subprocess

def desviacion_estandar(array):
    input_data = ','.join(f"{x}" for x in array) + '\n'  # Convertir array a string
    result = subprocess.run(['./desvAssembly'], input=input_data, text=True, capture_output=True)
    return result.returncode  # Convertir salida a entero

# Ejemplo de uso:
array = [45,2,74,8,3,56,0,1,25, 45, 125,6,569,788]
resultado = desviacion_estandar(array)
print(f"La desviacion estandar es: {resultado}")