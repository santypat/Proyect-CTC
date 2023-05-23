import os
import pandas as pd
# Ruta de la carpeta principal
ruta_principal = r"C:\Users\damian.pulgarin\OneDrive - arus.com.co\ASIGNACION PBS"

# Lista de nombres de las carpetas
carpetas = ["ARCHIVOS CTC", "CONSOLIDADO_PBS", "DIARIO", "RESULTADOS"]

# Verificar existencia de las carpetas
carpetas_faltantes = [carpeta for carpeta in carpetas if not os.path.exists(os.path.join(ruta_principal, carpeta))]

# Mostrar mensaje de error si faltan carpetas
if carpetas_faltantes:
    print("Error: Las siguientes carpetas no se encontraron:")
    for carpeta in carpetas_faltantes:
        print(carpeta)
    print("Por favor, verifique la existencia de las carpetas y vuelva a ejecutar el programa.")
else:
    print("Todas las carpetas existen. Puedes continuar con el programa.")

# cruce de archivos y actualizar columnas
# Código para cruzar los archivos según las condiciones mencionadas en el manual
# Actualizar las columnas correspondientes en el archivo "ARCHIVOS CTC"

def cruzar_archivos():
    # Cargar el archivo "CONSOLIDADO GENERAL PBS"
    
    #consolidado_pbs = pd.read_csv(r"C:\Users\damian.pulgarin\OneDrive - arus.com.co\ASIGNACION PBS\CONSOLIDADO_PBS\CONSOLIDADO_GENERAL_PBS.csv")
    filename = r"C:\Users\damian.pulgarin\OneDrive - arus.com.co\ASIGNACION PBS\CONSOLIDADO_PBS\CONSOLIDADO_GENERAL_PBS.csv"

# Leer el archivo CSV línea por línea y manejar las líneas problemáticas
    lines = []
    with open(filename, 'r') as file:
            for line in file:
                try:
                    data = line.strip().split(',')  # Ajusta el delimitador según corresponda
                    lines.append(data)
                except Exception as e:
                    print(f"Error en la línea: {line}")
                    print(f"Error: {e}")

# Convertir la lista de líneas en un DataFrame de pandas
    consolidado_pbs = pd.DataFrame(lines)

# Cargar el archivo "ARCHIVOS CTC"
archivos_excel_ctc = ['C:\\Users\\damian.pulgarin\\OneDrive - arus.com.co\\ASIGNACION PBS\\ARCHIVOS CTC\\INFORME-SAS-PENDIENTES-20230519062906.xls', 
                      'C:\\Users\\damian.pulgarin\\OneDrive - arus.com.co\\ASIGNACION PBS\\ARCHIVOS CTC\\INFORME-SAS-PENDIENTES-20230519062914.xls', 
                      'C:\\Users\\damian.pulgarin\\OneDrive - arus.com.co\\ASIGNACION PBS\\ARCHIVOS CTC\\INFORME-SAS-PENDIENTES-INTERNET-20230519062909.xls', 
                      'C:\\Users\\damian.pulgarin\\OneDrive - arus.com.co\\ASIGNACION PBS\\ARCHIVOS CTC\\INFORME-SAS-PENDIENTES-INTERNET-20230519062920.xls']
dtfs= []
for archivo in archivos_excel_ctc:
    archivos_ctc = pd.read_excel(archivo)
#archivos_ctc = pd.read_excel(archivos_excel_ctc)
    

# Realizar el cruce de los archivos
archivos_ctc["ENVIO A SURA"] = archivos_ctc["ENVIO A SURA"].apply(lambda x: "pendiente" if pd.isnull(x) or x == "PENDIENTE" else x)
archivos_ctc["RESPONSABLE"] = archivos_ctc["ASIGNACIÓN"].map({
        "AUX ARUS": "AUX ARUS",
        "AUX ARUS ANTICOAGULANTES": "AUX ARUS ANTICOAGULANTES",
        "AUX ARUS PROCEDIMIENTOS": "AUX ARUS PROCEDIMIENTOS",
        "QF ARUS": "QF ARUS",
        "QF ARUS POLIZA": "QF ARUS POLIZA",
        "MÉDICO": "MÉDICO",
        "ODONTOLOGIA": "ODONTOLOGIA"
    })
archivos_ctc["FECHA DE ENVIÓ ARUS"] = archivos_ctc.apply(
        lambda row: row["FECHA DE ENVIÓ ARUS"] if row["ENVIO A SURA"] != "pendiente" else "PTE ANDREA", axis=1)
archivos_ctc["NUMERO DE ENVIO"] = archivos_ctc["NUMERO DE ENVIO"].ffill().add(1)

    # Actualizar el archivo "ARCHIVOS CTC" con las columnas actualizadas
archivos_ctc.to_excel("ASIGNACION PBS/ARCHIVOS CTC/ARCHIVOS CTC.xlsx", index=False)

print("Cruce y actualización de columnas completados.")
# Llamada a la función para cruzar los archivos y actualizar las columnas
cruzar_archivos()


def generar_carpeta_asignacion():
    
    # Ruta de la carpeta "DIARIO"
    carpeta_diario = "ASIGNACION PBS/DIARIO"

    # Leer los archivos de la carpeta "DIARIO"
    archivos_diario = os.listdir(carpeta_diario)

    # Filtrar los archivos de Excel en la carpeta "DIARIO"
    archivos_excel = [archivo for archivo in archivos_diario if archivo.endswith(".xlsx")]

    # Recorrer los archivos de Excel y generar los archivos correspondientes
    for archivo in archivos_excel:
        # Obtener la fecha del archivo
        fecha_archivo = archivo.split(".")[0]  # Suponiendo que el nombre del archivo es la fecha sin extensión

        # Cargar el archivo de asignación del día
        asignacion_diaria = pd.read_excel(os.path.join(carpeta_diario, archivo))

        # Filtrar los registros por responsables y generar los archivos correspondientes
        asignacion_aux = asignacion_diaria[asignacion_diaria["RESPONSABLE"] == "AUX ARUS"]
        asignacion_qf = asignacion_diaria[asignacion_diaria["RESPONSABLE"] == "QF ARUS"]
        asignacion_odontologia = asignacion_diaria[asignacion_diaria["RESPONSABLE"] == "ODONTOLOGIA"]
        asignacion_poliza = asignacion_diaria[asignacion_diaria["RESPONSABLE"] == "QF ARUS POLIZA"]

        # Guardar los archivos generados en la carpeta "RESULTADOS"
        asignacion_aux.to_excel(f"ASIGNACION PBS/RESULTADOS/{fecha_archivo}_ASIGNACION_AUX.xlsx", index=False)
        asignacion_qf.to_excel(f"ASIGNACION PBS/RESULTADOS/{fecha_archivo}_ASIGNACION_QF.xlsx", index=False)
        asignacion_odontologia.to_excel(f"ASIGNACION PBS/RESULTADOS/{fecha_archivo}_ODONTOLOGIA.xlsx", index=False)
        asignacion_poliza.to_excel(f"ASIGNACION PBS/RESULTADOS/{fecha_archivo}_POLIZA.xlsx", index=False)

    print("Generación de la carpeta de asignación diaria completada.")
# Llamada a la función para generar la carpeta de asignación diaria
generar_carpeta_asignacion()


def completar_resultados():
    # Ruta de la carpeta "RESULTADOS"
    carpeta_resultados = "ASIGNACION PBS/RESULTADOS"

    # Leer los archivos de la carpeta "RESULTADOS"
    archivos_resultados = os.listdir(carpeta_resultados)

    # Filtrar los archivos de Excel en la carpeta "RESULTADOS"
    archivos_excel = [archivo for archivo in archivos_resultados if archivo.endswith(".xlsx")]

    # Recorrer los archivos de Excel y completar con el reparto
    for archivo in archivos_excel:
        # Cargar el archivo de asignación con los responsables
        asignacion_responsables = pd.read_excel(os.path.join(carpeta_resultados, archivo))

        # Cargar el archivo de reparto
        archivo_reparto = "ARCHIVO_REPARTO.xlsx"  # Reemplaza con el nombre y ruta correctos del archivo de reparto
        reparto = pd.read_excel(archivo_reparto)

        # Combinar los datos de asignación con el reparto mediante la columna clave
        asignacion_completa = pd.merge(asignacion_responsables, reparto, on="CLAVE", how="left")

        # Guardar el archivo completo en la carpeta "RESULTADOS"
        asignacion_completa.to_excel(os.path.join(carpeta_resultados, archivo), index=False)

    print("Completado de archivos con el reparto finalizado.")

# Llamada a la función para completar los archivos de la carpeta "RESULTADOS" con el reparto
completar_resultados()
pass

# Llamadas a las funciones según el flujo del programa
cruzar_archivos()
generar_carpeta_asignacion()
completar_resultados()

# Código posterior...
pp