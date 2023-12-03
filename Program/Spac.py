import os
import shutil
from datetime import datetime, timedelta
import zipfile

# Obtiene la ubicación del script actual
script_directory = os.path.dirname(os.path.abspath(__file__))

# Directorio donde se encuentra la carpeta de fotos (asumiendo que está en el mismo directorio que el script)
photo_directory = os.path.join(script_directory, "Foto-INTRUSO")

# Obtén la fecha actual
current_date = datetime.now()

# Calcula la fecha hace 7 días
seven_days_ago = current_date - timedelta(days=7)

# Lista de archivos en el directorio de fotos
photo_files = os.listdir(photo_directory)

for photo_file in photo_files:
    file_path = os.path.join(photo_directory, photo_file)
    
    # Obtiene la fecha de creación del archivo
    file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
    
    # Calcula la fecha 7 días después de la creación del archivo
    seven_days_after_creation = file_creation_time + timedelta(days=7)
    
    # Comprueba si la foto fue tomada hace 7 días después de su creación
    if current_date >= seven_days_after_creation:
        # Comprime la foto en un archivo ZIP
        zip_file_name = f"{photo_file}.zip"
        with zipfile.ZipFile(os.path.join(photo_directory, zip_file_name), 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(file_path, os.path.basename(file_path))
        