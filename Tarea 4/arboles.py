import os

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None
        self.altura = 1

class ABB:
    """Clase Base: Árbol Binario de Búsqueda"""
    def __init__(self):
        self.raiz = None

    def buscar(self, nodo, valor):
        if not nodo or nodo.valor == valor:
            return nodo
        if valor < nodo.valor:
            return self.buscar(nodo.izq, valor)
        return self.buscar(nodo.der, valor)

class AVL(ABB):
    """Clase Hija: Árbol AVL (Hereda de ABB)"""
    
    def get_altura(self, nodo):
        return nodo.altura if nodo else 0

    def get_balance(self, nodo):
        return self.get_altura(nodo.izq) - self.get_altura(nodo.der) if nodo else 0

    def rotar_derecha(self, y):
        x = y.izq
        T2 = x.der
        x.der = y
        y.izq = T2
        y.altura = 1 + max(self.get_altura(y.izq), self.get_altura(y.der))
        x.altura = 1 + max(self.get_altura(x.izq), self.get_altura(x.der))
        return x

    def rotar_izquierda(self, x):
        y = x.der
        T2 = y.izq
        y.izq = x
        x.der = T2
        x.altura = 1 + max(self.get_altura(x.izq), self.get_altura(x.der))
        y.altura = 1 + max(self.get_altura(y.izq), self.get_altura(y.der))
        return y

    def insertar(self, valor):
        self.raiz = self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        if not nodo:
            return Nodo(valor)
        
        if valor < nodo.valor:
            nodo.izq = self._insertar_recursivo(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._insertar_recursivo(nodo.der, valor)
        else:
            return nodo

        nodo.altura = 1 + max(self.get_altura(nodo.izq), self.get_altura(nodo.der))
        balance = self.get_balance(nodo)

        # Rotaciones para mantener el balance
        if balance > 1 and valor < nodo.izq.valor:
            return self.rotar_derecha(nodo)
        if balance < -1 and valor > nodo.der.valor:
            return self.rotar_izquierda(nodo)
        if balance > 1 and valor > nodo.izq.valor:
            nodo.izq = self.rotar_izquierda(nodo.izq)
            return self.rotar_derecha(nodo)
        if balance < -1 and valor < nodo.der.valor:
            nodo.der = self.rotar_derecha(nodo.der)
            return self.rotar_izquierda(nodo)

        return nodo

    def generar_graphviz(self):
        if not self.raiz:
            return "digraph G { empty [label='Arbol Vacio']; }"
        
        dot = ["digraph G {", "  node [shape=circle, fontname=Arial, color=blue, fontcolor=darkblue];"]
        self._recorrer_graphviz(self.raiz, dot)
        dot.append("}")
        return "\n".join(dot)

    def _recorrer_graphviz(self, nodo, dot):
        if nodo:
            if nodo.izq:
                dot.append(f'  {nodo.valor} -> {nodo.izq.valor};')
                self._recorrer_graphviz(nodo.izq, dot)
            if nodo.der:
                dot.append(f'  {nodo.valor} -> {nodo.der.valor};')
                self._recorrer_graphviz(nodo.der, dot)