import subprocess

# Datos para procesar
datos = [23, 45, 67, 89, 21, 34]

# Convertir los datos a una cadena separada por comas
contenido = ','.join(map(str, datos))

# Escribir los datos en el archivo de entrada
with open("entradaBaro.txt", "w") as archivo:
    archivo.write(contenido)

# Asegúrate de que el path al ejecutable es correcto
path_al_ejecutable = "./desviacion"

# Ejecutar el programa en ensamblador
result = subprocess.run([path_al_ejecutable], capture_output=True, text=True)

# Imprimir la salida y errores si los hay
print("Salida:", result.stdout)
print("Errores:", result.stderr)

# Leer el archivo de salida y mostrar los resultados
with open("Resul_des_bar.txt", "r") as file:
    output = file.read()
    print("Contenido del archivo de salida:", output)
