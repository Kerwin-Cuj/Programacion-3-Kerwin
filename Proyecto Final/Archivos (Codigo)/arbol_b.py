class PaginaPartida:
    def __init__(self, id_partida, resumen, tablero_final):
        self.id = id_partida
        self.resumen = resumen
        self.tablero = tablero_final

class NodoArbolB:
    def __init__(self, es_hoja=True):
        self.es_hoja = es_hoja
        self.claves = []
        self.hijos = []

class ArbolBHistorial:
    def __init__(self, degree=3):
        self.raiz = NodoArbolB(es_hoja=True)
        self.grado = degree

    def buscar(self, id_partida, nodo=None):
        if nodo is None:
            node = self.raiz
        else:
            node = nodo
        i = 0
        while i < len(node.claves) and id_partida > node.claves[i].id:
            i += 1
        if i < len(node.claves) and id_partida == node.claves[i].id:
            return node.claves[i]
        if node.es_hoja or len(node.hijos) == 0:
            return None
        return self.buscar(id_partida, node.hijos[i])

    def insertar(self, id_partida, resumen, tablero_final):
        nueva_partida = PaginaPartida(id_partida, resumen, tablero_final)
        raiz_actual = self.raiz
        if len(raiz_actual.claves) == (self.grado - 1):
            nuevo_nodo = NodoArbolB(es_hoja=False)
            self.raiz = nuevo_nodo
            nuevo_nodo.hijos.append(raiz_actual)
            self._dividir_hijo(nuevo_nodo, 0, raiz_actual)
            self._insertar_no_lleno(nuevo_nodo, nueva_partida)
        else:
            self._insertar_no_lleno(raiz_actual, nueva_partida)

    def _insertar_no_lleno(self, nodo, nueva_partida):
        i = len(nodo.claves) - 1
        if nodo.es_hoja or len(nodo.hijos) == 0:
            nodo.claves.append(None)
            while i >= 0 and nueva_partida.id < nodo.claves[i].id:
                nodo.claves[i + 1] = nodo.claves[i]
                i -= 1
            nodo.claves[i + 1] = nueva_partida
        else:
            while i >= 0 and nueva_partida.id < nodo.claves[i].id:
                i -= 1
            i += 1
            
            if i < 0:
                i = 0
            elif i >= len(nodo.hijos):
                i = len(nodo.hijos) - 1
                
            if len(nodo.hijos[i].claves) == (self.grado - 1):
                self._dividir_hijo(nodo, i, nodo.hijos[i])
                if nueva_partida.id > nodo.claves[i].id:
                    i += 1
            self._insertar_no_lleno(nodo.hijos[i], nueva_partida)

    def _dividir_hijo(self, nodo_padre, i, nodo_hijo):
        t = self.grado // 2
        nuevo_nodo = NodoArbolB(es_hoja=nodo_hijo.es_hoja)
        nodo_padre.hijos.insert(i + 1, nuevo_nodo)
        nodo_padre.claves.insert(i, nodo_hijo.claves[t])
        nuevo_nodo.claves = nodo_hijo.claves[t + 1:]
        nodo_hijo.claves = nodo_hijo.claves[:t]
        if not nodo_hijo.es_hoja and len(nodo_hijo.hijos) > 0:
            nuevo_nodo.hijos = nodo_hijo.hijos[t + 1:]
            nodo_hijo.hijos = nodo_hijo.hijos[:t + 1]

    def recorrer_historial(self, nodo=None, lista_resultado=None):
        if lista_resultado is None:
            lista_resultado = []
        if nodo is None:
            node = self.raiz
        else:
            node = nodo
        for i in range(len(node.claves)):
            if not node.es_hoja and len(node.hijos) > i:
                self.recorrer_historial(node.hijos[i], lista_resultado)
            lista_resultado.append(node.claves[i])
        if not node.es_hoja and len(node.hijos) > 0:
            self.recorrer_historial(node.hijos[-1], lista_resultado)
        return lista_resultado

    def graficar_arbol(self):
        dot_content = "digraph ArbolB {\n"
        dot_content += "    node [shape=record, bgcolor=white, fontname=\"Arial\"];\n"
        
        def generar_nodos_dot(nodo):
            if nodo is None:
                return ""
            
            id_nodo = str(id(nodo))
            etiqueta = "<f0> "
            for idx, clave in enumerate(nodo.claves):
                etiqueta += f"| ID: {clave.id}\\n{clave.resumen} | <f{idx+1}> "
            
            cuerpo = f"    \"{id_nodo}\" [label=\"{etiqueta}\"];\n"
            
            if not nodo.es_hoja:
                for idx, hijo in enumerate(nodo.hijos):
                    if hijo:
                        cuerpo += generar_nodos_dot(hijo)
                        cuerpo += f"    \"{id_nodo}\":f{idx} -> \"{id(hijo)}\";\n"
            return cuerpo

        dot_content += generar_nodos_dot(self.raiz)
        dot_content += "}\n"
        
        try:
            with open("reporte_arbol_b.dot", "w", encoding="utf-8") as f:
                f.write(dot_content)
            print("[Graphviz] Archivo 'reporte_arbol_b.dot' generado con éxito.")
            
            from graphviz import Source
            s = Source(dot_content)
            s.render("reporte_arbol_b", format="png", cleanup=True)
            print("[Graphviz] Imagen 'reporte_arbol_b.png' renderizada.")
        except Exception as e:
            print(f"[Graphviz Warning] No se pudo renderizar la imagen, pero se creó el archivo .dot técnico. Error: {e}")