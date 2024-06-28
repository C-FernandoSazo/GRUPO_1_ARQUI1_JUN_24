import subprocess

# Datos para procesar
datos_opcion1 = [23, 454, 675, 1958, 221, 34,1]
datos_opcion2 = [12, 341, 526, 78, 90, 11]

# Solicitar al usuario que elija una opción
opcion = input("Elige una opción (1 o 2): ")

# Validar la opción y asignar los datos correspondientes
if opcion == '1':
    datos = datos_opcion1
elif opcion == '2':
    datos = datos_opcion2
else:
    print("Opción no válida. Saliendo del programa.")
    exit(1)

# Convertir los datos a una cadena separada por comas
contenido = ','.join(map(str, datos)) + '\n'

with open("promedio.txt", "w") as archivo:
    archivo.write(contenido)

# Asegúrate de que el path al ejecutable es correcto
path_al_ejecutable = "./promedio"

# Ejecutar el programa en ensamblador, pasando los datos como argumento
result = subprocess.run([path_al_ejecutable], input=contenido, text=True, capture_output=True)

with open("respromedio.txt", "r") as file:
    output = file.read()
    print("Resultado", output)


