import pandas as pd

# Ruta de los archivos
ruta_carpeta = "C:\\Users\\damian.pulgarin\\OneDrive - arus.com.co\\ASIGNACION PBS"
ruta_archivo_consolidado = ruta_carpeta + "\\CONSOLIDADO_PBS\\CONSOLIDADO GENERAL PBS .csv"
ruta_archivo_diario = ruta_carpeta + "\\DIARIO"

# Cargar archivos
df_consolidado = pd.read_excel(ruta_archivo_consolidado)
df_diario = pd.read_excel(ruta_archivo_diario)

# Paso 1: Cruce con archivo CONSOLIDADO_GENERAL_PBS
df_consolidado["ENVIO A SURA"] = df_consolidado["ENVIO A SURA"].apply(lambda x: "pendiente" if x == "pendiente" else "envío t-")
df_consolidado["ENVÍO ARUS"] = df_consolidado["FECHA DE ENVÍO ARUS"].apply(lambda x: "actual" if pd.notnull(x) else "PTE ANDREA")
df_consolidado["NÚMERO DE ENVÍO"] = df_consolidado["NÚMERO DE ENVÍO"].apply(lambda x: x + 1)

# Paso 2: Cruce con archivo DIARIO
df_cruce = pd.merge(df_consolidado, df_diario, on=["RESPONSABLE", "ASIGNACIÓN", "FECHA DE ENVÍO ARUS"], how="left")
df_cruce.loc[df_cruce["AUTORIZAR_SN"].isin(["A", "G", "N", "P", "S", "SICODIGO"]), "ENVÍO T-"] = "envío t-"
df_cruce.loc[~df_cruce["AUTORIZAR_SN"].isin(["A", "G", "N", "P", "S", "SICODIGO"]), "ENVÍO T-"] = ""

df_cruce.loc[(df_cruce["AUTORIZAR_SN"] == "N") & (df_cruce["CAUSA_INACTIVACION"].notnull()), "ENVIOT"] = "enviot"
df_cruce.loc[(df_cruce["AUTORIZAR_SN"] != "N") & (df_cruce["CAUSA_INACTIVACION"].notnull()), "INCONSISTENCIASQF"] = "inconsistenciasqf"

# Guardar resultados en archivos
df_cruce.to_excel(ruta_carpeta + "/RESULTADOS/CRUZO.xlsx", index=False)
df_cruce.loc[df_cruce["ENVÍO T-"] == "", :].to_excel(ruta_carpeta + "/RESULTADOS/NO_CRUZO.xlsx", index=False)
df_cruce.loc[df_cruce["ENVÍO T-"] == "envío t-", :].to_excel(ruta_carpeta + "/RESULTADOS/enviot.xlsx", index=False)
df_cruce.loc[df_cruce["INCONSISTENCIASQF"] == "inconsistenciasqf", :].to_excel(ruta_carpeta + "/RESULTADOS/inconsistenciasqf.xlsx", index=False)

# Generar carpeta diaria de asignaciones
df_asignacion_aux = df_cruce[df_cruce["RESPONSABLE"] == "AUX ARUS"]
df_asignacion_qf = df_cruce[df_cruce["RESPONSABLE"] == "QF ARUS"]
df_odontologia = df_cruce[df_cruce["RESPONSABLE"] == "ODONTOLOGIA"]
df_poliza = df_cruce[df_cruce["RESPONSABLE"] == "POLIZA"]

df_asignacion_aux.to_excel(ruta_carpeta + "/RESULTADOS/ASIGNACION_AUX.xlsx", index=False)
df_asignacion_qf.to_excel(ruta_carpeta + "/RESULTADOS/ASIGNACION_QF.xlsx", index=False)
df_odontologia.to_excel(ruta_carpeta + "/RESULTADOS/ODONTOLOGIA.xlsx", index=False)
df_poliza.to_excel(ruta_carpeta + "/RESULTADOS/POLIZA.xlsx", index=False)

# Generar archivo de resumen de asignación
df_resumen_asignacion = pd.DataFrame({
    "RESPONSABLE": ["AUX ARUS", "QF ARUS", "ODONTOLOGIA", "POLIZA"],
    "ASIGNACIONES": [len(df_asignacion_aux), len(df_asignacion_qf), len(df_odontologia), len(df_poliza)]
})
df_resumen_asignacion.to_excel(ruta_carpeta + "/RESULTADOS/REPARTO.xlsx", index=False)
