import os
import csv

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(valor, self.raiz)

    def _insertar_recursivo(self, valor, nodo_actual):
        if valor < nodo_actual.valor:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = Nodo(valor)
            else:
                self._insertar_recursivo(valor, nodo_actual.izquierdo)
        elif valor > nodo_actual.valor:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = Nodo(valor)
            else:
                self._insertar_recursivo(valor, nodo_actual.derecho)

    def buscar(self, valor, nodo_actual=None, inicial=True):
        if inicial: nodo_actual = self.raiz
        if nodo_actual is None: return False
        if nodo_actual.valor == valor: return True
        
        if valor < nodo_actual.valor:
            return self.buscar(valor, nodo_actual.izquierdo, False)
        return self.buscar(valor, nodo_actual.derecho, False)

    def eliminar(self, valor):
        self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo, valor):
        if nodo is None: return nodo

        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, valor)
        else:
            if nodo.izquierdo is None: return nodo.derecho
            if nodo.derecho is None: return nodo.izquierdo
            
            temp = self._valor_minimo(nodo.derecho)
            nodo.valor = temp.valor
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, temp.valor)
        return nodo

    def _valor_minimo(self, nodo):
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    def generar_dot(self):
        dot = "digraph G {\n"
        dot += "  node [shape=circle, style=filled, fillcolor=lightblue, fontname=\"Arial\"];\n"
        if self.raiz:
            dot += self._retornar_nodos_dot(self.raiz)
        else:
            dot += '  "Arbol_Vacio" [label="Árbol Vacío", shape=none];\n'
        dot += "}"

        try:
           
            with open("arbol.dot", "w", encoding='utf-8') as f:
                f.write(dot)
            
            
            status = os.system("dot -Tpng arbol.dot -o arbol.png")
            
            if status == 0:
                print("\n[INFO] Imagen 'arbol.png' generada correctamente.")
                os.system("start arbol.png")
            else:
                print("\n[ERROR] No se pudo generar el PNG. Verifique la instalación de Graphviz.")
        except Exception as e:
            print(f"Error en el proceso gráfico: {e}")

    def _retornar_nodos_dot(self, nodo):
        contenido = ""
        if nodo.izquierdo:
            contenido += f'  "{nodo.valor}" -> "{nodo.izquierdo.valor}";\n'
            contenido += self._retornar_nodos_dot(nodo.izquierdo)
        if nodo.derecho:
            contenido += f'  "{nodo.valor}" -> "{nodo.derecho.valor}";\n'
            contenido += self._retornar_nodos_dot(nodo.derecho)
        return contenido


def menu():
    abb = ArbolBinarioBusqueda()
    while True:
        print("\n" + "="*40)
        print("      SISTEMA DE ÁRBOL BINARIO (UMG)     ")
        print("="*40)
        print("1. Insertar número")
        print("2. Buscar número")
        print("3. Eliminar número")
        print("4. Cargar desde archivo (.csv)")
        print("5. Salir")
        opcion = input("\nSeleccione una opción: ")

        if opcion == '1':
            try:
                num = int(input("Ingrese el número a insertar: "))
                abb.insertar(num)
                abb.generar_dot()
            except ValueError:
                print("Por favor, ingrese un número entero válido.")

        elif opcion == '2':
            try:
                num = int(input("Número a buscar: "))
                if abb.buscar(num):
                    print(f"¡El número {num} SÍ existe en el árbol!")
                else:
                    print(f"El número {num} NO se encuentra.")
            except ValueError:
                print("Entrada no válida.")

        elif opcion == '3':
            try:
                num = int(input("Número a eliminar: "))
                abb.eliminar(num)
                abb.generar_dot()
                print(f"Operación de eliminación realizada para: {num}")
            except ValueError:
                print("Entrada no válida.")

        elif opcion == '4':
            ruta = input("Nombre o ruta del archivo (ej: archivo1.csv): ").strip().replace('"', '')
            try:
                if os.path.exists(ruta):
                    with open(ruta, newline='', encoding='utf-8') as f:
                        lector = csv.reader(f)
                        for fila in lector:
                            for dato in fila:
                                if dato.strip():
                                    abb.insertar(int(dato.strip()))
                    print("Datos cargados exitosamente.")
                    abb.generar_dot()
                else:
                    print("Error: El archivo no existe en la carpeta del proyecto.")
            except Exception as e:
                print(f"Ocurrió un error al leer el archivo: {e}")

        elif opcion == '5':
            print("Cerrando el programa. ¡Éxito en su entrega!")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    menu()