# Proyect-CTC

#este codigo sirve para la apertura de la carpeta :

def abrir_carpeta_ubicada_en_escritorio(carpeta_nombre):
    escritorio_path = os.path.join(os.path.expanduser("~"), "Desktop")
    carpeta_path = os.path.join(escritorio_path, carpeta_nombre)
    
    try:
        os.startfile(carpeta_path)
    except OSError as e:
        print(f"No se pudo abrir la carpeta: {e}")

# Nombre de la carpeta que deseas abrir en el escritorio
carpeta_nombre = "Nombre de la carpeta"

# Llamar a la función para abrir la carpeta
abrir_carpeta_ubicada_en_escritorio(carpeta_nombre)"""


