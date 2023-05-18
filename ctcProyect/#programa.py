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


