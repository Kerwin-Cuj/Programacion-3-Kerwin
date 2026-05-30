import tkinter as tk
from tkinter import messagebox, ttk

class VentanaTotito:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Proyecto Final - Totito Inteligente (UMG)")
        self.root.geometry("500x630")
        self.root.resizable(False, False)
        self.botones_tablero = []
        self.crear_interfaz_principal()

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def crear_interfaz_principal(self):
        self.limpiar_pantalla()
        lbl_titulo = tk.Label(self.root, text=" MENU TOTITO KERWIN 🎮", font=("Arial", 20, "bold"), fg="#1a237e")
        lbl_titulo.pack(pady=25)
        
        lbl_contador = tk.Label(self.root, text=f"Partidas jugadas en la sesión: {self.controlador.contador_partidas}", font=("Arial", 11, "italic"))
        lbl_contador.pack(pady=5)

        btn_manual = tk.Button(self.root, text="1. Entrenamiento Manual (Jugar)", font=("Arial", 12), width=35, bg="#e3f2fd", command=self.iniciar_juego_manual)
        btn_manual.pack(pady=10)

        btn_auto = tk.Button(self.root, text="2. Entrenamiento Automático (Simulación)", font=("Arial", 12), width=35, bg="#e8f5e9", command=self.seccion_entrenamiento_automatico)
        btn_auto.pack(pady=10)

        btn_historial = tk.Button(self.root, text="3. Consultar Historial (Árbol B)", font=("Arial", 12), width=35, bg="#fff3e0", command=self.ver_historial_arbol_b)
        btn_historial.pack(pady=10)

        btn_creditos = tk.Button(self.root, text="4. Créditos de Desarrollador", font=("Arial", 12), width=35, bg="#f3e5f5", command=self.mostrar_creditos)
        btn_creditos.pack(pady=10)

        btn_salir = tk.Button(self.root, text="Salir", font=("Arial", 12), width=15, bg="#ffebee", command=self.root.quit)
        btn_salir.pack(pady=25)

    def iniciar_juego_manual(self):
        self.limpiar_pantalla()
        self.botones_tablero = []
        
        lbl_juego = tk.Label(self.root, text="Tu turno! Eres 'X'", font=("Arial", 16, "bold"))
        lbl_juego.pack(pady=15)
        
        frame_tablero = tk.Frame(self.root)
        frame_tablero.pack(pady=10)
        
        for i in range(9):
            fila = i // 3
            columna = i % 3
            btn = tk.Button(frame_tablero, text=" ", font=("Arial", 24, "bold"), width=5, height=2, bg="#ffffff",
                            command=lambda pos=i: self.presionar_casilla(pos))
            btn.grid(row=fila, column=columna, padx=5, pady=5)
            self.botones_tablero.append(btn)
            
        btn_volver = tk.Button(self.root, text="Volver al Menú", command=self.crear_interfaz_principal)
        btn_volver.pack(pady=20)

    def presionar_casilla(self, posicion):
        if self.controlador.tablero.marcar_movimiento(posicion, "X"):
            self.botones_tablero[posicion].config(text="X", fg="#1565c0", state="disabled")
            resultado = self.controlador.tablero.verificar_ganador()
            if resultado:
                self.procesar_fin_juego(resultado)
                return
            
            pos_ia = self.controlador.jugar_turno_ia(simbolo_ia="O")
            self.botones_tablero[pos_ia].config(text="O", fg="#c62828", state="disabled")
            resultado = self.controlador.tablero.verificar_ganador()
            if resultado:
                self.procesar_fin_juego(resultado)

    def procesar_fin_juego(self, resultado):
        if resultado == "X":
            messagebox.showinfo("Fin del Juego", "¡Ganaste! La IA aprenderá de este error.")
            self.controlador.finalizar_partida("Perdió IA")
        elif resultado == "O":
            messagebox.showinfo("Fin del Juego", " ¡La IA ha ganado!")
            self.controlador.finalizar_partida("Ganó IA")
        elif resultado == "Empate":
            messagebox.showinfo("Fin del Juego", "¡Es un empate!")
            self.controlador.finalizar_partida("Empate")
        self.crear_interfaz_principal()

    def seccion_entrenamiento_automatico(self):
        self.limpiar_pantalla()
        lbl_auto = tk.Label(self.root, text="🤖 Entrenamiento Automático", font=("Arial", 16, "bold"))
        lbl_auto.pack(pady=20)
        
        lbl_instruccion = tk.Label(self.root, text="Iteraciones a simular:", font=("Arial", 11))
        lbl_instruccion.pack(pady=10)
        
        txt_cantidad = tk.Entry(self.root, font=("Arial", 12), width=15, justify="center")
        txt_cantidad.pack(pady=5)
        txt_cantidad.insert(0, "1000")

        def ejecutar_simulacion():
            try:
                cant = int(txt_cantidad.get())
                if cant <= 0: raise ValueError
                self.controlador.simular_partidas_automaticas(cant)
                messagebox.showinfo("Éxito", f"Simuladas {cant} partidas con éxito.")
                self.crear_interfaz_principal()
            except ValueError:
                messagebox.showerror("Error", "Ingresa un número entero positivo.")

        btn_entrenar = tk.Button(self.root, text="Iniciar Simulación", font=("Arial", 11, "bold"), bg="#4caf50", fg="white", command=ejecutar_simulacion)
        btn_entrenar.pack(pady=20)
        btn_volver = tk.Button(self.root, text="Volver al Menú", command=self.crear_interfaz_principal)
        btn_volver.pack(pady=10)

    def ver_historial_arbol_b(self):
        self.limpiar_pantalla()
        lbl_hist = tk.Label(self.root, text="📚 Historial Guardado (Árbol B)", font=("Arial", 16, "bold"))
        lbl_hist.pack(pady=15)
        
        lista_partidas = self.controlador.historial_arbol_b.recorrer_historial()
        columnas = ("id", "resumen", "tablero")
        tabla = ttk.Treeview(self.root, columns=columnas, show="headings", height=10)
        tabla.heading("id", text="ID Partida")
        tabla.heading("resumen", text="Resumen")
        tabla.heading("tablero", text="Tablero Final")
        
        tabla.column("id", width=100, anchor="center")
        tabla.column("resumen", width=220, anchor="w")
        tabla.column("tablero", width=120, anchor="center")
        
        for p in lista_partidas:
            tabla.insert("", tk.END, values=(p.id, p.resumen, p.tablero))
            
        tabla.pack(pady=10, padx=15, fill="both", expand=True)
        
        def disparar_grafico():
            self.controlador.historial_arbol_b.graficar_arbol()
            messagebox.showinfo("Graphviz", "Estructura exportada a la raíz como 'reporte_arbol_b.dot' y archivo .png")

        btn_graficar = tk.Button(self.root, text=" Generar Gráfico de Estructura (Graphviz)", font=("Arial", 10, "bold"), bg="#009688", fg="white", command=disparar_grafico)
        btn_graficar.pack(pady=5)
        
        btn_volver = tk.Button(self.root, text="Volver al Menú", command=self.crear_interfaz_principal)
        btn_volver.pack(pady=10)

    def mostrar_creditos(self):
        self.limpiar_pantalla()
        lbl_cred = tk.Label(self.root, text="🎓 Datos del Desarrollador", font=("Arial", 16, "bold"))
        lbl_cred.pack(pady=30)
        
        info = (
            "Universidad Mariano Gálvez de Guatemala\n"
            "Facultad de Ingeniería en Sistemas\n"
            "Programación III - Quinto Semestre 2026\n\n"
            "Desarrollador: Kerwin Israel Cuj Pernillo\n"
            "Sección: A\n\n"
            "Porcentaje de Participación: 100% (Individual)"
        )
        lbl_info = tk.Label(self.root, text=info, font=("Arial", 11), justify="center", bg="#f9f9f9", padx=20, pady=20, borderwidth=1, relief="solid")
        lbl_info.pack(pady=10)
        btn_volver = tk.Button(self.root, text="Volver al Menú", command=self.crear_interfaz_principal)
        btn_volver.pack(pady=30)