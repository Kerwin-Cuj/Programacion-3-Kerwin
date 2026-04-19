import os
from arboles import AVL
from utils import leer_datos_csv, generar_imagen_png

class Arbol_AVL_Kerwin:
    def __init__(self):
        self.arbol = AVL()

    def cargar_desde_csv(self, nombre_archivo):
        datos = leer_datos_csv(nombre_archivo)
        if datos:
            for valor in datos:
                self.arbol.insertar(valor)
            print(f" Se cargaron {len(datos)} elementos.")

    def exportar_visualizacion(self):
        contenido_dot = self.arbol.generar_graphviz()
        nombre_dot = "arbol_resultado.dot"
        nombre_png = "arbol_resultado.png"
        
        with open(nombre_dot, "w") as f:
            f.write(contenido_dot)
        
        # Llama a la funcion de utils que genera y abre la imagen
        generar_imagen_png(nombre_dot, nombre_png)

    def mostrar_menu(self):
        while True:
            print("\n========================================")
            print("   SISTEMA DE ARBOL AVL - KERWIN (UMG)  ")
            print("========================================")
            print("1. Insertar numero")
            print("2. Buscar numero")
            print("3. Cargar datos desde CSV")
            print("4. Generar imagen Graphviz")
            print("5. Salir")
            print("========================================")
            
            opcion = input("Seleccione una opcion: ")
            
            if opcion == "1":
                try:
                    val = int(input("Ingrese el numero a insertar: "))
                    self.arbol.insertar(val)
                    print(f" {val} insertado con exito.")
                except ValueError:
                    print(" Por favor, ingrese solo numeros enteros.")
            
            elif opcion == "2":
                try:
                    val = int(input("Numero a buscar: "))
                    encontrado = self.arbol.buscar(self.arbol.raiz, val)
                    if encontrado:
                        print(f" El numero {val} SI se encuentra en el arbol.")
                    else:
                        print(f" El numero {val} NO existe en el arbol.")
                except ValueError:
                    print(" Entrada no valida.")
            
            elif opcion == "3":
                nombre = input("Nombre del archivo (ej: datos1.csv): ")
                self.cargar_desde_csv(nombre)
            
            elif opcion == "4":
                self.exportar_visualizacion()
            
            elif opcion == "5":
                print(" Cerrando programa...")
                break
            else:
                print(" Opcion no valida, intente de nuevo.")

if __name__ == "__main__":
    app = Arbol_AVL_Kerwin()
    app.mostrar_menu()