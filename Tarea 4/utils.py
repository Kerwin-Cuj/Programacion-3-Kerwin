import csv
import subprocess
import os

def leer_datos_csv(nombre_archivo):
    """Lee una lista de enteros desde un archivo CSV."""
    valores = []
    try:
        if not os.path.exists(nombre_archivo):
            print(f" Error: El archivo '{nombre_archivo}' no existe.")
            return []
        
        with open(nombre_archivo, mode='r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                for dato in fila:
                    if dato.strip():
                        valores.append(int(dato.strip()))
        return valores
    except ValueError:
        print(" Error: El archivo contiene datos que no son numeros enteros.")
        return []
    except Exception as e:
        print(f" Error inesperado: {e}")
        return []

def generar_imagen_png(nombre_dot, nombre_png):
    """Convierte un archivo .dot a .png y lo abre automaticamente."""
    try:
        subprocess.run(["dot", "-Tpng", nombre_dot, "-o", nombre_png], check=True)
        print(f" Imagen '{nombre_png}' generada con exito.")
        
        if os.name == 'nt': # Windows
            os.startfile(nombre_png)
        else: # Linux o Mac
            subprocess.run(["xdg-open", nombre_png] if os.name == 'posix' else ["open", nombre_png])
            
    except Exception as e:
        print(f"Error: No se pudo mostrar la imagen.. {e}")