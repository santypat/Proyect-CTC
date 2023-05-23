# Proyect-CTC-DIAGRAMA DE FLUJO

Inicio
├─ Verificar existencia de carpetas
│   ├─ ¿Existe la carpeta "archivos ctc"?
│   │   ├─ Sí ──┐
│   │   │       ├─ ¿Existe la carpeta "consolidado_pbs"?
│   │   │       ├─ ¿Existe la carpeta "diario"?
│   │   │       ├─ ¿Existe la carpeta "resultados"?
│   │   │       └─ Realizar el proceso de asignación y generación de archivos
│   │   └─ No ──┐
│   │           └─ Detener el programa y mostrar mensaje de error
│   ├─ ¿Existe la carpeta "consolidado_pbs"?
│   ├─ ¿Existe la carpeta "diario"?
│   └─ ¿Existe la carpeta "resultados"?
├─ Realizar los cruces con los archivos descargados
│   ├─ ¿La columna "DESCRIPCION_PRESTACION" contiene "APIXABAN", "DABIGATRAN" o "RIVAROXABAN"?
│   │   ├─ Sí ──┐
│   │   │       ├─ Actualizar columnas específicas para asignar tarea al equipo "AUX ARUS ANTICOAGULANTES"
│   │   │       └─ Continuar con el siguiente paso
│   │   └─ No ──┐
│   │           ├─ Buscar en el dataframe "MALLA PX NO PBS.csv" coincidencia entre "SURACUPS" y "CODIGO_PRESTACION"   
│   │           ├─ ¿Se encontró una coincidencia?
│   │           │   ├─ Sí ──┐
│   │           │   │       ├─ ¿El valor de la columna 6 en la coincidencia es "ARUS verificar criterios PBS"?
│   │           │   │       │   ├─ Sí ──┐
│   │           │   │       │   │       ├─ Asignar tarea al equipo "AUX ARUS"
│   │           │   │       │   │       └─ Actualizar columnas específicas
│   │           │   │       │   └─ No ──┐
│   │           │   │       │           ├─ ¿El valor de la columna 6 en la coincidencia es "Odontología PBS"?
│   │           │   │       │           │   ├─ Sí ──┐
│   │           │   │       │           │   │       ├─ Asignar tarea al equipo "ODONTOLOGIA"
│   │           │   │       │           │   │       └─ Actualizar columnas específicas
│   │           │   │       │           │   └─ No ──┐
│   │           │   │       │           │           ├─ ¿El valor de la columna 6 en la coincidencia es "Verificar Auditoria Inclusiones" o "Verificar Auditoria inclusiones No frecuencia"?
│   │           │   │       │           │           │   ├─ Sí ──┐
│   │           │   │       │           │           │   │       ├─ Asignar tarea al equipo "AUDITORIA INCLUSIONES"
│   │           │   │       │           │           │   │       └─ Actualizar columnas específicas
│   │           │   │       │           │           │   └─ No ──┐
│   │           │   │       │           │           │           └─ Asignar tarea al equipo "AUX SERVICIOS"
│   │           │   │       │           │           └─────────┐
│   │           │   │       │           │                       └─ Actualizar columnas específicas
│   │           │   │       │           └─────────────────┐
│   │           │   │       │                               └─ No hacer nada
│   │           │   │       └─ Continuar con el siguiente paso
│   │           │   └─ No ──┐
│   │           │           └─ Asignar tarea al equipo "AUX SERVICIOS"
│   │           └─────────┐
│   │                       └─ Actualizar columnas específicas
│   └─ Continuar con el siguiente paso
└─ Guardar los archivos generados en la carpeta "resultados"


 


