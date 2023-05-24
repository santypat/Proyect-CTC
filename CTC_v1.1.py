import os
import pandas as pd
import glob

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
    filename = r"C:\Users\damian.pulgarin\OneDrive - arus.com.co\ASIGNACION PBS\CONSOLIDADO_PBS\CONSOLIDADO GENERAL PBS .csv"

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
ruta_base = 'C:\\Users\\damian.pulgarin\\OneDrive - arus.com.co\\ASIGNACION PBS\\ARCHIVOS CTC\\'
patron = 'INFORME-SAS-PENDIENTES-*.xls'

archivos_excel_ctc = glob.glob(ruta_base + patron)

# Nombre del archivo de consolidado general PBS
archivo_consolidado = 'C:\\Users\\damian.pulgarin\\OneDrive - arus.com.co\\ASIGNACION PBS\\CONSOLIDADO_PBS\\CONSOLIDADO GENERAL PBS .csv'

# Columnas relevantes para el cruce
columnas_relevantes = ['ENVIO A SURA', 'RESPONSABLE', 'ASIGNACIÓN', 'FECHA DE ENVIÓ ARUS', 'NUMERO DE ENVIO']

# Leer el archivo de consolidado general PBS
df_consolidado = pd.read_csv(archivo_consolidado, delimiter=';', low_memory=False)

# Obtener el número de envío actual
num_envio_actual = df_consolidado['NUMERO DE ENVIO'].max() + 1

# Iterar sobre los archivos de la carpeta CTC
for ruta_archivo in archivos_excel_ctc:
    if ruta_archivo.endswith('.xlsx'):
        df_ctc = pd.read_excel(ruta_archivo, usecols=columnas_relevantes)

        # Filtrar las filas según los criterios mencionados
        filtro_envio_sura = df_ctc['ENVIO A SURA'].str.contains('pendiente|nuevo', case=False, na=False)
        filtro_responsable = df_ctc['RESPONSABLE'].str.contains('AUX ARUS|QF ARUS|QF POLIZA', case=False, na=False)
        filtro_fecha_envio = df_ctc['FECHA DE ENVIÓ ARUS'].str.contains('PTE ANDREA', case=False, na=False)

        # Actualizar las filas que cumplan los criterios
        df_ctc.loc[filtro_envio_sura, 'ENVIO A SURA'] = 'pendiente'
        df_ctc.loc[filtro_responsable, 'RESPONSABLE'] = 'AUX ARUS / QF ARUS / QF POLIZA'
        df_ctc.loc[filtro_fecha_envio & ~filtro_envio_sura, 'FECHA DE ENVIÓ ARUS'] = pd.to_datetime(df_ctc['G']).dt.strftime('%d/%m/%Y')
        df_ctc.loc[filtro_fecha_envio & filtro_envio_sura, 'FECHA DE ENVIÓ ARUS'] = pd.to_datetime(df_ctc['G']).dt.strftime('%d/%m/%Y')
        df_ctc.loc[~filtro_fecha_envio & ~filtro_envio_sura, 'NUMERO DE ENVIO'] = num_envio_actual

        # Concatenar el DataFrame procesado al consolidado
        df_consolidado = pd.concat([df_consolidado, df_ctc], ignore_index=True)

        # Incrementar el número de envío actual
        num_envio_actual += 1

# Guardar el consolidado final en un nuevo archivo
archivo_consolidado_final = 'CONSOLIDADO_GENERAL_PBS_FINAL.xlsx'
df_consolidado.to_excel(archivo_consolidado_final, index=False)