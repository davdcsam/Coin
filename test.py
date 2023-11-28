import os

# Obtener la ruta de la carpeta AppData
appdata_path = os.getenv('APPDATA')

print(appdata_path)

program_files_path = os.getenv('PROGRAMFILES')

print(program_files_path)