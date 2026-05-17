from btree import BTree
from utils import load_csv

def main():
    print("=== Proyecto Árbol B Kerwin ===")
    grado = int(input("Ingrese el grado del Árbol B: "))
    grado_max = grado - 1
    grado_min = grado_max // 2

    print(f"Grado máximo: {grado_max}, Grado mínimo: {grado_min}")

    btree = BTree(grado_min, grado_max)

    while True:
        print("\n--- Menú Árbol B Kerwin ---")
        print("1. Insertar clave")
        print("2. Buscar clave")
        print("3. Eliminar clave")
        print("4. Cargar CSV")
        print("5. Exportar gráfico")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            clave = input("Ingrese la clave: ")
            btree.insert(clave)
        elif opcion == "2":
            clave = input("Ingrese la clave a buscar: ")
            print("Encontrada" if btree.search(clave) else "No encontrada")
        elif opcion == "3":
            clave = input("Ingrese la clave a eliminar: ")
            btree.delete(clave)
        elif opcion == "4":
            archivo = input("Ingrese nombre del archivo CSV: ")
            datos = load_csv(archivo)
            for d in datos:
                btree.insert(d)
            print(f"Se cargaron {len(datos)} registros desde {archivo}")
            # Mostrar gráfico inmediatamente
            dot = btree.export_graphviz()
            dot.render("ArbolBKerwin_graph", format="png", view=True)
        elif opcion == "5":
            dot = btree.export_graphviz()
            dot.render("ArbolBKerwin_graph", format="png", view=True)
            print("Gráfico exportado y abierto en pantalla.")
        elif opcion == "6":
            break

if __name__ == "__main__":
    main()
    input("Presiona Enter para salir...")
