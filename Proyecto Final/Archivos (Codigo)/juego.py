import random
from estructuras.historial_partida import ListaHistorial
from estructuras.tablero import TableroTotito
from estructuras.arbol_b import ArbolBHistorial

class ControladorJuego:
    def __init__(self, arbol_instancia):
        self.arbol_decision = arbol_instancia
        self.tablero = TableroTotito()
        self.historial_arbol_b = ArbolBHistorial()
        self.historial_partida = ListaHistorial()
        self.derrotas_consecutivas = 0
        self.factor_aprendizaje = 1.0
        self.contador_partidas = 0

    def registrar_movimiento_ia(self, estado_string, casilla):
        self.historial_partida.insertar(estado_string, casilla)

    def jugar_turno_ia(self, simbolo_ia="O"):
        estado_previo = self.tablero.clonar_estado()
        casilla_elegida = self.arbol_decision.obtener_mejor_movimiento(self.tablero, self.derrotas_consecutivas)
        self.tablero.marcar_movimiento(casilla_elegida, simbolo_ia)
        self.registrar_movimiento_ia(estado_previo, casilla_elegida)
        return casilla_elegida

    def finalizar_partida(self, resultado_vista):
        self.contador_partidas += 1
        base_puntos = 400
        tablero_final_str = self.tablero.clonar_estado()
        
        if resultado_vista == "Perdió IA":
            self.derrotas_consecutivas += 1
            self.factor_aprendizaje = 1.0 + (self.derrotas_consecutivas * 1.5)
            puntos_ajuste = base_puntos * self.factor_aprendizaje
            self.actualizar_pesos_retrogrados(-puntos_ajuste)
            # Corregido a .insertar()
            self.historial_arbol_b.insertar(self.contador_partidas, "Derrota de la IA - Dificultad Escalada", tablero_final_str)
        elif resultado_vista == "Ganó IA":
            self.derrotas_consecutivas = 0
            self.factor_aprendizaje = 1.0
            self.actualizar_pesos_retrogrados(base_puntos)
            # Corregido a .insertar()
            self.historial_arbol_b.insertar(self.contador_partidas, "Victoria de la IA", tablero_final_str)
        elif resultado_vista == "Empate":
            self.factor_aprendizaje += 0.5
            self.actualizar_pesos_retrogrados(base_puntos * 0.5)
            # Corregido a .insertar()
            self.historial_arbol_b.insertar(self.contador_partidas, "Empate", tablero_final_str)

        # GENERACIÓN AUTOMÁTICA DE GRAPHVIZ PARA LA EVOLUCIÓN DE LA ESTRATEGIA:
        self.arbol_decision.graficar_estrategia(self.contador_partidas)

        self.historial_partida.vaciar()
        self.tablero.reiniciar_tablero()

    def actualizar_pesos_retrogrados(self, puntos):
        nodo_actual = self.historial_partida.primero
        while nodo_actual is not None:
            self.arbol_decision.modificar_peso_nodo(
                nodo_actual.estado, 
                nodo_actual.movimiento, 
                puntos
            )
            nodo_actual = nodo_actual.siguiente

    def simular_partidas_automaticas(self, iteraciones):
        for _ in range(iteraciones):
            self.tablero.reiniciar_tablero()
            self.historial_partida.vaciar()
            juego_terminado = False
            turno_ia = random.choice([True, False])
            
            while not juego_terminado:
                estado_previo = self.tablero.clonar_estado()
                if turno_ia:
                    casilla = self.arbol_decision.obtener_mejor_movimiento(self.tablero, 0)
                    self.tablero.marcar_movimiento(casilla, "O")
                    self.registrar_movimiento_ia(estado_previo, casilla)
                else:
                    vacias = []
                    for i in range(9):
                        c = self.tablero.obtener_casilla(i)
                        if c and c.valor == " ":
                            vacias.append(i)
                    if vacias:
                        casilla = random.choice(vacias)
                        self.tablero.marcar_movimiento(casilla, "X")
                
                res = self.verify_ganador_interno()
                if res:
                    juego_terminado = True
                    self.contador_partidas += 1
                    if res == "O":
                        self.actualizar_pesos_retrogrados(400)
                        self.historial_arbol_b.insertar(self.contador_partidas, "Simulación: Ganó IA", self.tablero.clonar_estado())
                    elif res == "X":
                        self.actualizar_pesos_retrogrados(-400 * 1.5)
                        self.historial_arbol_b.insertar(self.contador_partidas, "Simulación: Perdió IA", self.tablero.clonar_estado())
                    else:
                        self.actualizar_pesos_retrogrados(200)
                        self.historial_arbol_b.insertar(self.contador_partidas, "Simulación: Empate", self.tablero.clonar_estado())
                turno_ia = not turno_ia
                
            # Genera el diagrama de Graphviz al terminar cada partida de la simulación
            self.arbol_decision.graficar_estrategia(self.contador_partidas)
                
        self.historial_partida.vaciar()
        self.tablero.reiniciar_tablero()

    def verify_ganador_interno(self):
        combinaciones = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        )
        for combo in combinaciones:
            v0 = self.tablero.obtener_casilla(combo[0]).valor
            v1 = self.tablero.obtener_casilla(combo[1]).valor
            v2 = self.tablero.obtener_casilla(combo[2]).valor
            if v0 != " " and v0 == v1 == v2:
                return v0
        actual = self.tablero.cabeza
        while actual:
            if actual.valor == " ":
                return None
            actual = actual.siguiente
        return "Empate"