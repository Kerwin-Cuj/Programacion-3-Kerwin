class NodoHistorial:
    def __init__(self, estado_tablero, movimiento_ia):
        self.estado = estado_tablero
        self.movimiento = movimiento_ia
        self.siguiente = None

class ListaHistorial:
    def __init__(self):
        self.primero = None
    
    def insertar(self, estado, movimiento):
        nuevo = NodoHistorial(estado, movimiento)
        if not self.primero:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def vaciar(self):
        self.primero = None
