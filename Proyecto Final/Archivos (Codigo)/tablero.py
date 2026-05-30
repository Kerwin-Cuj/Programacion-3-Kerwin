class NodoCasilla:
    def __init__(self, posicion):
        self.posicion = posicion
        self.valor = " "
        self.siguiente = None

class TableroTotito:
    def __init__(self):
        self.cabeza = None
        self._construir_tablero()

    def _construir_tablero(self):
        self.cabeza = NodoCasilla(0)
        actual = self.cabeza
        for i in range(1, 9):
            nuevo_nodo = NodoCasilla(i)
            actual.siguiente = nuevo_nodo
            actual = nuevo_nodo

    def obtener_casilla(self, posicion):
        actual = self.cabeza
        while actual:
            if actual.posicion == posicion:
                return actual
            actual = actual.siguiente
        return None

    def marcar_movimiento(self, posicion, jugador):
        casilla = self.obtener_casilla(posicion)
        if casilla and casilla.valor == " ":
            casilla.valor = jugador
            return True
        return False

    def reiniciar_tablero(self):
        actual = self.cabeza
        while actual:
            actual.valor = " "
            actual = actual.siguiente

    def clonar_estado(self):
        estado = ""
        actual = self.cabeza
        while actual:
            estado += actual.valor if actual.valor != " " else "-"
            actual = actual.siguiente
        return estado

    def verificar_ganador(self):
        combinaciones = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        )
        for combo in combinaciones:
            v0 = self.obtener_casilla(combo[0]).valor
            v1 = self.obtener_casilla(combo[1]).valor
            v2 = self.obtener_casilla(combo[2]).valor
            if v0 != " " and v0 == v1 == v2:
                return v0
        actual = self.cabeza
        while actual:
            if actual.valor == " ":
                return None
            actual = actual.siguiente
        return "Empate"
