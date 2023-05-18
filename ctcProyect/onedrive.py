import pyonedrive
import os

carpeta ='C:\\Users\\damian.pulgarin\\OneDrive - arus.com.co\\ASIGNACION PBS'
archivos = os.listdir(carpeta)

for archivo in archivos:
    ruta_archivo = os.path.join(carpeta, archivo)
    with open(ruta_archivo, 'r') as f:
        contenido = f.read()
        
        print(contenido)