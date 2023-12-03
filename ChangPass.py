import subprocess
import os

# Nombre del archivo a buscar
nombre_archivo = "Conf.py"

# Ruta absoluta del directorio del script actual
directorio_script = os.path.dirname(os.path.abspath(__file__))

# Función para buscar el archivo de forma recursiva
def buscar_archivo(directorio):
    for item in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, item)
        if os.path.isdir(ruta_completa):
            resultado = buscar_archivo(ruta_completa)
            if resultado:
                return resultado
        elif item == nombre_archivo:
            return ruta_completa
    return None

# Busca el archivo
ruta_archivo = buscar_archivo(directorio_script)

# Ejecuta el archivo si se encuentra
if ruta_archivo:
    subprocess.run(["python", ruta_archivo])
else:
    print("Archivo no encontrado.")
