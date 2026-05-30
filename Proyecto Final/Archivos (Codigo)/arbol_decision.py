class ArbolDecision:
    def __init__(self):
        self.memoria_pesos = {}

    def buscar_peso_estado_hijo(self, estado_string, movimiento):
        if estado_string in self.memoria_pesos:
            if movimiento in self.memoria_pesos[estado_string]:
                return self.memoria_pesos[estado_string][movimiento]
        return 0 

    def obtener_mejor_movimiento(self, tablero_totito, derrotas_consecutivas):
        estado_string = tablero_totito.clonar_estado()

        if derrotas_consecutivas >= 2:
            movimiento_bloqueo = self._buscar_bloqueo_inmediato(tablero_totito)
            if movimiento_bloqueo is not None:
                print(f"[IA MODO CRÍTICO] Bloqueando casilla: {movimiento_bloqueo}")
                return movimiento_bloqueo

        mejor_movimiento = None
        max_peso = -999999
        
        for mov in range(9):
            casilla = tablero_totito.obtener_casilla(mov)
            if casilla and casilla.valor == " ":
                peso_camino = self.buscar_peso_estado_hijo(estado_string, mov)
                if peso_camino > max_peso:
                    max_peso = peso_camino
                    mejor_movimiento = mov
                
        if max_peso == 0 or mejor_movimiento is None:
            mejor_movimiento = self._prioridad_posicional(tablero_totito)

        return mejor_movimiento

    def _prioridad_posicional(self, tablero_totito):
        c_centro = tablero_totito.obtener_casilla(4)
        if c_centro and c_centro.valor == " ": 
            return 4
        for esquina in [0, 2, 6, 8]:
            c_esq = tablero_totito.obtener_casilla(esquina)
            if c_esq and c_esq.valor == " ": 
                return esquina
        for lado in [1, 3, 5, 7]:
            c_lad = tablero_totito.obtener_casilla(lado)
            if c_lad and c_lad.valor == " ": 
                return lado
        for i in range(9):
            c_aux = tablero_totito.obtener_casilla(i)
            if c_aux and c_aux.valor == " ":
                return i
        return 0

    def _buscar_bloqueo_inmediato(self, tablero_totito):
        lineas_ganadoras = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for linea in lineas_ganadoras:
            cuenta_humano = 0
            espacio_vacio = None
            for pos in linea:
                val = tablero_totito.obtener_casilla(pos).valor
                if val == 'X':
                    cuenta_humano += 1
                elif val == ' ':
                    espacio_vacio = pos
            if cuenta_humano == 2 and espacio_vacio is not None:
                return espacio_vacio
        return None

    def modificar_peso_nodo(self, estado, movimiento, puntos):
        if estado not in self.memoria_pesos:
            self.memoria_pesos[estado] = {}
        if movimiento not in self.memoria_pesos[estado]:
            self.memoria_pesos[estado][movimiento] = 0
        self.memoria_pesos[estado][movimiento] += puntos
        print(f"[Árbol] Peso Actualizado -> Estado: {estado} | Jugada: {movimiento} | Peso: {self.memoria_pesos[estado][movimiento]} pts")

    def graficar_estrategia(self, id_partida):
        dot_content = "digraph EvolucionEstrategia {\n"
        dot_content += "    node [shape=ellipse, style=filled, fillcolor=\"#e3f2fd\", fontname=\"Arial\"];\n"
        dot_content += f"    label=\"Evolución de Estrategia - Partida ID: {id_partida}\\n(Pesos de Aprendizaje de la IA)\";\n"
        dot_content += "    labelloc=\"t\";\n"
        
        if not self.memoria_pesos:
            dot_content += "    \"Sin datos\" [label=\"El árbol no ha aprendido movimientos aún.\", shape=box];\n"
        else:
            for estado, movimientos in self.memoria_pesos.items():
                id_estado = estado.replace("-", "_")
                label_tablero = f"Tablero: {estado}"
                dot_content += f"    \"{id_estado}\" [label=\"{label_tablero}\", fillcolor=\"#fff3e0\", shape=box];\n"
                
                for mov, peso in movimientos.items():
                    id_hijo = f"{id_estado}_m{mov}"
                    dot_content += f"    \"{id_hijo}\" [label=\"Jugada: {mov}\\nPeso: {peso} pts\", fillcolor=\"#e8f5e9\"];\n"
                    dot_content += f"    \"{id_estado}\" -> \"{id_hijo}\" [label=\"Decisión\"];\n"
                    
        dot_content += "}\n"
        
        try:
            nombre_archivo = f"reporte_estrategia_partida_{id_partida}"
            with open(f"{nombre_archivo}.dot", "w", encoding="utf-8") as f:
                f.write(dot_content)
            
            from graphviz import Source
            s = Source(dot_content)
            s.render(nombre_archivo, format="png", cleanup=True)
            print(f"[Graphviz] Gráfico de estrategia generado: {nombre_archivo}.png")
        except Exception as e:
            print(f"[Graphviz Warning] No se pudo renderizar la imagen de la estrategia: {e}")