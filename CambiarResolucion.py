import os
import json
from tkinter import Tk, filedialog

# Archivo de configuración para guardar el directorio seleccionado
CONFIG_FILE = "config.json"

def save_last_directory(directory):
    config = {"last_directory": directory}
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config, config_file)

def load_last_directory():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            config = json.load(config_file)
            return config.get("last_directory", "")
    return ""

def edit_resolutions(file_path, width, height):
    # Verificar y remover la protección de solo lectura
    if not os.access(file_path, os.W_OK):
        os.chmod(file_path, 0o644)

    # Leer el archivo
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Parámetros a actualizar
    keys_x = [
        "ResolutionSizeX",
        "LastUserConfirmedResolutionSizeX",
        "LastUserConfirmedDesiredScreenWidth",
        "DesiredScreenWidth"
    ]
    keys_y = [
        "ResolutionSizeY",
        "LastUserConfirmedResolutionSizeY",
        "LastUserConfirmedDesiredScreenHeight",
        "DesiredScreenHeight"
    ]

    # Actualizar las líneas correspondientes
    for i, line in enumerate(lines):
        for key in keys_x:
            if line.strip().startswith(key):
                lines[i] = f"{key}={width}\n"
        for key in keys_y:
            if line.strip().startswith(key):
                lines[i] = f"{key}={height}\n"

    # Escribir los cambios de vuelta al archivo
    with open(file_path, 'w') as file:
        file.writelines(lines)

    # Restaurar la protección de solo lectura
    os.chmod(file_path, 0o444)
    print(f"Archivo editado y configurado como solo lectura: {file_path}")

# Ejemplo de uso
if __name__ == "__main__":
    # Cargar último directorio utilizado
    last_directory = load_last_directory()

    # Crear ventana para seleccionar archivo
    Tk().withdraw()  # Ocultar la ventana principal de Tk
    ini_file_path = filedialog.askopenfilename(
        title="Seleccionar archivo .ini",
        initialdir=last_directory if last_directory else None,
        filetypes=[("Archivos INI", "*.ini")]
    )

    if not ini_file_path:
        print("No se seleccionó ningún archivo.")
    else:
        # Guardar el directorio del archivo seleccionado
        save_last_directory(os.path.dirname(ini_file_path))

        # Dimensiones deseadas
        new_width = input("Ingresa el nuevo ancho de la pantalla: ").strip()
        new_height = input("Ingresa la nueva altura de la pantalla: ").strip()

        try:
            new_width = int(new_width)
            new_height = int(new_height)

            # Editar el archivo
            edit_resolutions(ini_file_path, new_width, new_height)
        except ValueError:
            print("Por favor, ingresa valores válidos para ancho y altura.")
        except FileNotFoundError:
            print(f"El archivo {ini_file_path} no fue encontrado.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")
