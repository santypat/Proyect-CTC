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

##########################################################################################################
##########################################################################################################
##########################################################################################################

# Obtener la ruta del último archivo creado
ruta_diario = 'C:\\Users\\damian.pulgarin\\OneDrive - arus.com.co\\ASIGNACION PBS\\DIARIO'
ultimo_archivo = max(os.listdir(ruta_diario), key=os.path.getctime)
ruta_ultimo_archivo = os.path.join(ruta_diario, ultimo_archivo)

# Leer el archivo del consolidado general PBS
df_consolidado = pd.read_csv(archivo_consolidado, delimiter=';', low_memory=False)

# Leer el último archivo del diario
df_diario = pd.read_excel(ruta_ultimo_archivo)

# Columnas relevantes para el cruce
columnas_relevantes_consolidado = ['ENVIO A SURA', 'RESPONSABLE', 'ASIGNACIÓN', 'FECHA DE ENVIÓ ARUS', 'NUMERO DE ENVIO']
columnas_relevantes_diario = ['AUTORIZAR_SN', 'OBSERVACIONES', 'CAUSA_INACTIVACION', 'RESPONSABLE', 'ASIGNACIÓN', 'FECHA ENVIO ARUS']

# Realizar el cruce del consolidado con el último archivo del diario
df_cruce = pd.merge(df_consolidado[columnas_relevantes_consolidado], df_diario[columnas_relevantes_diario], on=['RESPONSABLE', 'ASIGNACIÓN', 'FECHA ENVIO ARUS'], how='left')

# Guardar el resultado del cruce en un nuevo archivo
archivo_resultado = 'CRUCE_CONSOLIDADO_DIARIO.xlsx'
df_cruce.to_excel(archivo_resultado, index=False)

#######################################################
########################################################
#########################################################

# Columnas relevantes para el cruce con asignaciones
columnas_relevantes_asignacion = ['AUTORIZAR_SN', 'OBSERVACIONES', 'CAUSA_INACTIVACION']

# Realizar el cruce del consolidado con el último archivo del diario (asignaciones)
df_cruce_asignacion = pd.merge(df_consolidado, df_diario[columnas_relevantes_asignacion], left_on='ASIGNACIÓN', right_on='AUTORIZAR_SN', how='left')

# Carpeta "RESULTADOS" para guardar los archivos generados
ruta_resultados = 'C:\\Users\\damian.pulgarin\\OneDrive - arus.com.co\\ASIGNACION PBS\\RESULTADOS'

# Crear las carpetas dentro de "RESULTADOS" si no existen
carpetas_resultados = ['CRUZO', 'enviot', 'inconsistenciasqf', 'NO CRUZO', 'nocruzoEnvioVSConpbs', 'REPARTO']
for carpeta in carpetas_resultados:
    ruta_carpeta = os.path.join(ruta_resultados, carpeta)
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

# Filtrar las filas según las condiciones de las columnas y guardar en los archivos correspondientes
df_cruce_asignacion['AUTORIZAR_SN'] = df_cruce_asignacion['AUTORIZAR_SN'].astype(str).str.strip()
df_cruce_asignacion['OBSERVACIONES'] = df_cruce_asignacion['OBSERVACIONES'].astype(str).str.strip()

# Filtro para las columnas B y C
filtro_B = df_cruce_asignacion['AUTORIZAR_SN'].isin(['A', 'G', 'N', 'P', 'S', 'SICODIGO'])
filtro_C = df_cruce_asignacion['OBSERVACIONES'].isin(['PRESCRIPCIÓN ERRADA', 'LA INDICACIÓN DE USO DEL MEDICAMENTO NO ESTÁ APROBADA POR EL INVIMA', 'MEDICAMENTO AGOTADO/DESABASTECIDO', 'SUPERA DOSIS FARMACOLÓGICA', 'NO INDICADO PARA EDAD', 'EXISTE EVIDENCIA DE INTERACCIÓN O REACCIÓN MEDICAMENTOSA', 'NO SE ENCUENTRAN SOPORTES', 'PRESTACIÓN YA AUTORIZADA', 'EXCLUSIÓN DEL PLAN DE BENEFICIOS EN SALUD (TEMAS ESTÉTICOS)', 'JUSTIFICACIÓN INSUFICIENTE', 'PRESCRIPCIÓN REQUIERE SEGUNDO CONCEPTO', 'PRESCRIPCIÓN SUPERA ETAPA DE TRATAMIENTO', 'SOPORTES INSUFICIENTES O INCORRECTOS', 'PENDIENTE VALIDACIÓN ENFERMEDAD HUÉRFANA'])

# Generar los archivos correspondientes según las condiciones
df_cruce_asignacion[filtro_B].to_excel(os.path.join(ruta_resultados, 'enviot', 'Archivo_envio_t.xlsx'), index=False)
df_cruce_asignacion[~filtro_B].to_excel(os.path.join(ruta_resultados, 'inconsistenciasqf', 'Archivo_inconsistenciasqf.xlsx'), index=False)
df_cruce_asignacion[filtro_B & filtro_C].to_excel(os.path.join(ruta_resultados, 'enviot', 'Archivo_enviot.xlsx'), index=False)
df_cruce_asignacion[~filtro_B | ~filtro_C].to_excel(os.path.join(ruta_resultados, 'inconsistenciasqf', 'Archivo_inconsistenciasqf.xlsx'), index=False)

# Resto del proceso para generar los archivos en la carpeta "RESULTADOS" (carpetas CRUZO, NO CRUZO, nocruzoEnvioVSConpbs, REPARTO, etc.)
# ...
