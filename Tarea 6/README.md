Proyecto Árbol B Kerwin en Python

Kerwin Israel Cuj Pernillo
Carnet:9490-24-12144
Seccion: A

---

-Descripción
Este proyecto implementa un Árbol B en Python, con soporte para:
- Inserción de claves
- Búsqueda de claves
- Carga de datos desde archivos CSV
- Exportación y visualización gráfica con Graphviz

El objetivo es mostrar cómo funciona un Árbol B y poder visualizarlo de manera práctica.


Instrucciones de uso
1. Abrir el proyecto en Visual Studio 2019.
2. Ejecutar el archivo `main.py`.
3. Ingresar el grado del Árbol B cuando el sistema lo solicite.
   - El programa calcula automáticamente:
     - Grado máximo = grado ingresado - 1
     - Grado mínimo = grado máximo / 2
4. Usar el menú interactivo para:
   - Insertar claves manualmente
   - Buscar claves
   - Eliminar claves (pendiente de implementación)
   - Cargar datos desde CSV
   - Exportar y visualizar el gráfico del Árbol B

---

-Archivos CSV
El proyecto incluye tres archivos de prueba:
- `data1.csv` = números del 1 al 150
- `data2.csv` = códigos alfanuméricos (A001, A002, … A150)
- `data3.csv` = usuarios (user001, user002, … user150)

Estos archivos se pueden cargar desde el menú con la opción 4 (Cargar CSV).


Representación gráfica
El Árbol B se exporta y se abre automáticamente en pantalla usando Graphviz
