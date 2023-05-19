#programa
import os

carpeta_principal = os.path.join(os.path.expanduser("~"), "Desktop", "ASIGNACION PBS")
carpetas_secundarias = ["ARCHIVOS CTC", "CONSOLIDADO_PBS", "DIARIO", "RESULTADOS"]

# Verificar si la carpeta principal existe
if not os.path.exists(carpeta_principal):
    print("La carpeta principal no existe")
    exit()

# Verificar la existencia de las carpetas secundarias
carpetas_faltantes = []
for carpeta_secundaria in carpetas_secundarias:
    carpeta_actual = os.path.join(carpeta_principal, carpeta_secundaria)
    if not os.path.exists(carpeta_actual):
        carpetas_faltantes.append(carpeta_secundaria)

# Mostrar los resultados
if len(carpetas_faltantes) == 0:
    print("Todas las carpetas se encontraron correctamente.")
else:
    print("Las siguientes carpetas no coinciden o no existen:")
    for carpeta_faltante in carpetas_faltantes:
        print(carpeta_faltante)

import os

def obtener_archivos_ctc():
    carpeta_ctc = os.path.join(carpeta_principal, "ARCHIVOS CTC")
    archivos_ctc = os.listdir(carpeta_ctc)
    return archivos_ctc

def procesar_asignacion():
    archivo_asignacion = os.path.join(carpeta_principal, "CONSOLIDADO_PBS", "ASIGNACION")
    # Procesar el archivo de asignación y determinar responsables
    # Código adicional aquí
    pass

def verificar_duplicados():
    archivo_duplicados = os.path.join(carpeta_principal, "CONSOLIDADO_PBS", "CONSOLIDADO ENVIOS DUPLICADOS")
    # Verificar duplicados y obtener recuento
    # Código adicional aquí
    pass

# Definir las demás funciones según sea necesario

# Código original
carpeta_principal = os.path.join(os.path.expanduser("~"), "Desktop", "ASIGNACION PBS")
carpetas_secundarias = ["ARCHIVOS CTC", "CONSOLIDADO_PBS", "DIARIO", "RESULTADOS"]

# Verificar si la carpeta principal existe
if not os.path.exists(carpeta_principal):
    print("La carpeta principal no existe")
    exit()

# Verificar la existencia de las carpetas secundarias
carpetas_faltantes = []
for carpeta_secundaria in carpetas_secundarias:
    carpeta_actual = os.path.join(carpeta_principal, carpeta_secundaria)
    if not os.path.exists(carpeta_actual):
        carpetas_faltantes.append(carpeta_secundaria)

# Mostrar los resultados
if len(carpetas_faltantes) == 0:
    print("Todas las carpetas se encontraron correctamente.")
else:
    print("Las siguientes carpetas no coinciden o no existen:")
    for carpeta_faltante in carpetas_faltantes:
        print(carpeta_faltante)

# Llamar a las funciones adicionales
archivos_ctc = obtener_archivos_ctc()
print("Archivos CTC encontrados:", archivos_ctc)

procesar_asignacion()

verificar_duplicados()

# Llamar a las demás funciones según sea necesario



