import sys

# --- Funciones Recursivas ---

def convertir_a_binario(n):
    if n == 0:
        return "0"
    elif n == 1:
        return "1"
    else:
        return convertir_a_binario(n // 2) + str(n % 2)

def contar_digitos(n):
    n = abs(n)  # Manejar números negativos
    if n < 10:
        return 1
    return 1 + contar_digitos(n // 10)

def raiz_cuadrada_entera(n):
    if n < 0:
        return "Error: No se puede calcular la raíz de un número negativo."
    
    def calcular_raiz_cuadrada(n, estimacion):
        if (estimacion + 1) ** 2 > n:
            return estimacion
        return calcular_raiz_cuadrada(n, estimacion + 1)
    
    return calcular_raiz_cuadrada(n, 0)

def convertir_a_decimal(romano):
    valores = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    romano = romano.upper()
    
    if len(romano) == 0:
        return 0
    if len(romano) == 1:
        return valores[romano[0]]
    
    if valores[romano[0]] < valores[romano[1]]:
        return valores[romano[1]] - valores[romano[0]] + convertir_a_decimal(romano[2:])
    else:
        return valores[romano[0]] + convertir_a_decimal(romano[1:])

def suma_numeros_enteros(n):
    if n <= 0:
        return 0
    return n + suma_numeros_enteros(n - 1)

# --- Interfaz de Línea de Comandos (CLI) ---

def mostrar_menu():
    print("\n--- MENÚ INTERACTIVO: RECURSIVIDAD ---")
    print("1. Convertir a Binario")
    print("2. Contar Dígitos")
    print("3. Raíz Cuadrada Entera")
    print("4. Convertir a Decimal desde Romano")
    print("5. Suma de Números Enteros")
    print("6. Salir")
    return input("Seleccione una opción: ")

def ejecutar_programa():
    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            num = int(input("Ingrese un número entero positivo: "))
            print(f"Resultado Binario: {convertir_a_binario(num)}")
        
        elif opcion == "2":
            num = int(input("Ingrese un número: "))
            print(f"Cantidad de dígitos: {contar_digitos(num)}")
            
        elif opcion == "3":
            num = int(input("Ingrese el número para calcular su raíz: "))
            print(f"Raíz cuadrada entera: {raiz_cuadrada_entera(num)}")
            
        elif opcion == "4":
            rom = input("Ingrese el número romano (ej. XIV): ")
            try:
                print(f"Equivalente Decimal: {convertir_a_decimal(rom)}")
            except KeyError:
                print("Error: El texto ingresado no es un número romano válido.")
                
        elif opcion == "5":
            num = int(input("Suma hasta el número: "))
            print(f"La suma total es: {suma_numeros_enteros(num)}")
            
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    ejecutar_programa()

