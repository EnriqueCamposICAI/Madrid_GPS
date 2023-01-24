from typing import List, Tuple, Dict
import networkx as nx
import sys
import heapq
import matplotlib.pyplot as plt

INFTY = sys.float_info.max


class Vertice(object):

    def __init__(self, index: int):
        self.adyacencia = []
        self.indice = index


class Arista(object):

    def __init__(self, origen: Vertice, destino: Vertice,
                 data_arista: object, peso: float):
        '''Inicializa los objetos de la clase arista

        Args:
            origen: Objeto de la clase Vértice que, en el caso de que el grafo
            sea dirigido, designará el vértice de salida
            destino: Objeto de la clase Vértice que
            tiene el comportamiento contrario al origen
            data: Objeto que el usuario podrá proporcionar a la hora de la
            inicialización para almacenar distinta información como ¿?
            peso: Número en coma flotante, que designa
            el costo de "atravesar" la arista

        Returns
            None
        '''
        self.origen = origen
        self.destino = destino
        self.data_arista = data_arista
        self.peso = peso


class Grafo:
    # Diseñar y construirl a clase grafo

    def __init__(self, dirigido):
        """ Crea un grafo dirigido o no dirigido.

        Args:
            dirigido: Flag que indica si el grafo es dirigido o no.
        Returns: Grafo o grafo dirigido (según lo indicado por el flag)
        inicializado sin vértices ni aristas.
            vertices: Diccionario que almacena los vértices del grafo {objeto: objeto Vertice}
            aristas: Lista que almacena las aristas del grafo
        """
        self.dirigido = dirigido
        self.vertices = {}
        self.aristas = []

        pass

    # Operaciones básicas del TAD
    def es_dirigido(self) -> bool:
        """ Indica si el grafo es dirigido o no

        Args: None
        Returns: True si el grafo es dirigido, False si no.
        """
        return self.dirigido

    def agregar_vertice(self, v: object) -> None:
        """ Agrega el vértice v al grafo.

        Args:
            v: vértice que se quiere agregar.
        Returns:
            None
        """
        if v not in self.vertices.keys():
            # Se cre y añade el vertice
            self.vertices[v] = Vertice(len(self.vertices))

        return None

    def agregar_arista(self, s: object, t: object, data: object,
                       weight: float = 1) -> None:
        """ Si los objetos s y t son vértices del grafo, agrega
        una arista al grafo que va desde el vértice s hasta el vértice t
        y le asocia los datos "data" y el peso weight.
        En caso contrario, no hace nada.

        Args:
            s: vértice de origen (source)
            t: vértice de destino (target)
            data: datos de la arista
            weight: peso de la arista
        Returns:
             None
        """

        if not self.dirigido:
            self.vertices[s].adyacencia.append(
                t)       # Se añaden a la adyacencia
            self.vertices[t].adyacencia.append(s)
            aris = Arista(s, t, data, weight)           # Se crea la arista
            # Se añade a la lista de aristas
            self.aristas.append(aris)
            aris = Arista(t, s, data, weight)
            self.aristas.append(aris)

        else:
            # Para grafos dirigidos (solo hay una arista)
            self.vertices[s].adyacencia.append(t)
            aris = Arista(s, t, data, weight)
            self.aristas.append(aris)

        return None

    def eliminar_vertice(self, v: object) -> None:
        """ Si el objeto v es un vértice del grafo lo elimiina.
        Si no, no hace nada.

        Args: v vértice que se quiere eliminar
        Returns: None
        """

        try:
            # Hay que cambiar los indices
            self.vertices.pop(v)
            vertex = list(self.vertices.keys())     # Vértices restantes
            for i in range(len(vertex)):
                # Si el vertice esta en la adyacencia
                if v in self.vertices[vertex[i]].adyacencia:
                    self.vertices[vertex[i]].adyacencia.remove(v)   # Se quita

                self.vertices[vertex[i]].indice = i + \
                    1       # Se actualizan los indices

            self.aristas = [
                a for a in self.aristas if a.origen != v and a.destino != v]        # Se quitan las aristas
            return None
        except ValueError:      # Si no existe el vertice
            return None

    def eliminar_arista(self, s: object, t: object) -> None:
        """ Si los objetos s y t son vértices del grafo y existe
        una arista de u a v la elimina.
        Si no, no hace nada.

        Args:
            s: vértice de origen de la arista
            t: vértice de destino de la arista
        Returns: None
        """
        i = 0

        # Se recorre la lista de aristas, si la encuentra la elimina, si no, pasa a la siguiente

        while i < len(self.aristas):
            if self.aristas[i].origen == s and self.aristas[i].destino == t:
                self.aristas.pop(i)
                self.vertices[s].adyacencia.remove(t)
            elif self.aristas[i].origen == t and self.aristas[i].destino == s:
                self.aristas.pop(i)
                self.vertices[t].adyacencia.remove(s)
            else:
                i += 1

        return None

    def obtener_arista(self, s: object, t: object) -> Tuple[
            object, float] or None:
        """ Si los objetos s y t son vértices del grafo y existe
        una arista de u a v, devuelve sus datos y su peso en una tupla.
        Si no, devuelve None

        Args:
            s: vértice de origen de la arista
            t: vértice de destino de la arista
        Returns: Una tupla (a,w) con los datos de la arista "a" y su peso
        "w" si la arista existe. None en caso contrario.
        """

        # Si encuentra la arista, devueqlve los datos y el peso

        for i in range(len(self.aristas)):
            if self.aristas[i].origen == s and self.aristas[i].destino == t:
                return (self.aristas[i].data_arista, self.aristas[i].peso)

        return None

    def lista_adyacencia(self, u: object) -> List[object] or None:
        """ Si el objeto u es un vértice del grafo, devuelve
        su lista de adyacencia.
        Si no, devuelve None.

        Args: u vértice del grafo
        Returns: Una lista [v1,v2,...,vn] de los vértices del grafo
        adyacentes a u si u es un vértice del grafo y None en caso
        contrario
        """

        if u in self.vertices.keys():
            return self.vertices[u].adyacencia
        else:
            return None

    # Grados de vértices

    def grado_saliente(self, v: object) -> int or None:
        """ Si el objeto u es un vértice del grafo, devuelve
        su grado saliente.
        Si no, devuelve None.

        Args: u vértice del grafo
        Returns: El grado saliente (int) si el vértice existe y
        None en caso contrario.
        """

        if v in self.vertices.keys():
            return len(self.vertices[v].adyacencia)
        else:
            return None

    def grado_entrante(self, v: object) -> int or None:
        """ Si el objeto u es un vértice del grafo, devuelve
        su grado entrante.
        Si no, devuelve None.

        Args: u vértice del grafo
        Returns: El grado entrante (int) si el vértice existe y
        None en caso contrario.
        """

        # Se cuenta el número de veces que aparece en en la lisa de adyacencia de los vértices

        if v in self.vertices.keys():
            entrantes = 0
            for u in self.vertices.keys():
                if v in self.vertices[u].adyacencia:
                    entrantes += 1
            return entrantes
        else:
            return None

    def grado(self, v: object) -> int or None:
        """ Si el objeto u es un vértice del grafo, devuelve
        su grado si el grafo no es dirigido y su grado saliente si
        es dirigido.
        Si no pertenece al grafo, devuelve None.

        Args: u vértice del grafo
        Returns: El grado (int) o grado saliente (int) según corresponda
        si el vértice existe y None en caso contrario.
        """
        if v in self.vertices.keys():
            return self.grado_saliente(v)
        else:
            return None

    # Algoritmos

    def dijkstra(self, origen: object) -> Dict[object, object]:
        """ Calcula un Árbol Abarcador Mínimo para el grafo partiendo
        del vértice "origen" usando el algoritmo de Dijkstra.
        Calcula únicamente el árbol de la componente
        conexa que contiene a "origen".

        Args: origen vértice del grafo de origen
        Returns: Devuelve un diccionario que indica,
        para cada vértice alcanzable desde "origen",
        qué vértice es su padre en el árbol abarcador mínimo.
        """

        padre, visitado, dist = {}, {}, {}
        for vertex in list(self.vertices.keys()):
            # Inicializamos padres, vértices y visitados
            # de cada vértice usando diccionarios
            padre[vertex] = None
            visitado[vertex] = False
            dist[vertex] = INFTY

        dist[origen] = 0  # Del origen al origen, no hay distancia
        i = 0
        Q = [(dist[origen], i, origen)]
        i += 1

        # Lista de prioridad ordenada por d
        while len(Q):

            # Extraemos el elemento v con menor distancia de Q

            v = heapq.heappop(Q)[2]

            # Con lo programado en las 3 líneas anteriores, queremos saber
            # cuál es el par (clave, valor) que debemos borrar (aquel que
            # tiene el mayor valor de distancia)

            if not visitado[v]:
                visitado[v] = True
                for w in self.vertices[v].adyacencia:
                    # Si no hemos visitado el vertice, comprobamos las distancias a los otros vertices adyacentes
                    arista = self.obtener_arista(v, w)
                    # Se compara con la que tenemos hasta el momento + esa arista
                    # Si es menor se cambia y añade a la lista de prioridad
                    if dist[v] + arista[1] < dist[w]:
                        dist[w] = dist[v] + arista[1]
                        padre[w] = v
                        heapq.heappush(
                            Q, (dist[w], i, w))
                        i += 1

        return padre

    def camino_minimo(self, origen: object, destino: object) -> List[object]:
        '''Calcula el camino mínimo entre dos vértices pertenecientes al grafo
        mediante el Algoritmo Dijkstra. Puesto que Dijkstra devuelve un
        diccionario con los padres de cada vértices con items (objeto_vertice:
        objeto_vertice), deberemos inferir de este resultado general el camino
        local entre origen y destino. Para ello, recorreremos de manera inversa
        los padres, partiendo del destino y llegando al origen

        Args: origen vértice del grafo de origen
              destino vértice del grafo de destino

        Returns: Devuelve una tupla cuyos elementos son una lista con los
        vértices a visitar (en orden) y el coste total de este camino. Si no existe el camino desde origen hasta destino, devuelve (None, None)
        '''

        # Vamos al padre de cada vertice hasta llegar al origen

        padre = self.dijkstra(origen)
        # Sacamos djikistra desde el origen

        if destino not in padre.keys():     # Si el destino no está en el dict, no hay camino
            return (None, None)
        else:
            coste = 0
            camino = [destino]
            actual = destino
            # Vamos recorriendo el árbol de caminos mínimos hasta llegar al origen
            while actual != origen:
                proximo = padre[actual]
                camino.append(proximo)
                coste += self.obtener_arista(actual, proximo)[1]
                actual = proximo

            return (camino[::-1], coste)

    def prim(self) -> Dict[object, object]:
        """ Calcula un Árbol Abarcador Mínimo para el grafo
        usando el algoritmo de Prim.

        Args: None
        Returns: Devuelve un diccionario que indica, para cada vértice del
        grafo, qué vértice es su padre en el árbol abarcador mínimo.
        """
        padre, coste_minimo = {}, {}
        Q = []
        heapq.heapify(Q)  # Lista de prioridad ordenada por coste_minimo
        for vertex in self.vertices.keys():
            # Inicializamos su padre como nulo y su coste mínimo infinito
            padre[vertex] = None
            coste_minimo[vertex] = INFTY
            # Añadimos a nuestra lista de prioridad el vértice
            heapq.heappush(Q, (coste_minimo[vertex], vertex))
        while Q:
            # Extraemos aquel vértice con menor coste_minimo
            heapq.heapify(Q)
            v = heapq.heappop(Q)[1]

            # Iteramos sólo en aquellos vértices que estén en la adyacencia de
            # v y no hayan sido recorridos todavía
            # Creamos union Nv y Q:
            lista_vertices = [x[1] for x in Q]

            NvnQ = [x for x in self.vertices[v].adyacencia if x in lista_vertices]

            for w in NvnQ:

                # Si la arista tiene un peso menor que la que hay hasta ahora
                # para llegar a w, su coste se actualizará
                aris_dat = self.obtener_arista(v, w)
                if aris_dat[1] < coste_minimo[w]:
                    coste_minimo[w] = aris_dat[1]
                    padre[w] = v
                    for par in Q:
                        if par[1] == self.vertices[w].indice:
                            par[0] = coste_minimo[w]
                            break
        return padre

    def kruskal(self) -> List[Tuple[object, object]]:
        """ Calcula un Árbol Abarcador Mínimo para el grafo
        usando el algoritmo de Prim.

        Args: None
        Returns: Devuelve una lista [(s1,t1),(s2,t2),...,(sn,tn)]
        de los pares de vértices del grafo
        que forman las aristas del arbol abarcador mínimo.
        """
        copy_aristas, sol = self.aristas.copy(), []
        # Usamos list comprehension para hacer una lista relacionada
        peso_aristas = [arista.peso for arista in copy_aristas]
        L = []  # Contendrá las aristas ordenadas por peso de - a +
        while copy_aristas:
            # Encontremos la arista con menor peso
            idx = peso_aristas.index(min(peso_aristas))
            # La añadimos al final de la lista L ordenada
            L.append(copy_aristas[idx])
            peso_aristas.pop(idx)
            copy_aristas.pop(idx)

        C = {v: [v] for v in self.vertices.keys()}

        while L:  # Mientras que L no esté vacío
            # Extraemos la arista de menor peso
            a = L.pop(0)
            u, v = a.origen, a.destino  # Vértices de origen y destino de A
            if C[u] != C[v]:

                sol.append((u, v))
                # Unificar componentes de u y v -> C[u] U C[v]
                C[u] = C[u] + C[v]
                C[v] = C[u]
                for w in C[v]:
                    C[w] = C[u]

        return sol

    # NetworkX

    def convertir_a_NetworkX(self) -> nx.Graph or nx.DiGraph:
        """ Construye un grafo o digrafo de Networkx según corresponda
        a partir de los datos del grafo actual.

        Args: None
        Returns: Devuelve un objeto Graph de NetworkX si el grafo es
        no dirigido y un objeto DiGraph si es dirigido. En ambos casos,
        los vértices y las aristas son los contenidos en el grafo dado.
        """

        # Se define el Grafo
        if self.dirigido:
            G = nx.DiGraph()
        else:
            G = nx.Graph()

        # Se añaden los vértices
        G.add_nodes_from(self.vertices.keys())

        # Las aristsa hay que añadirlas una a una
        for aris in self.aristas:
            G.add_edge(aris.origen, aris.destino,
                       object=aris.data_arista, weight=aris.peso)

        return G

    def camino_minimo_mejorado(self, origen, destino):
        '''Calcula el camino mínimo entre dos vértices pertenecientes al grafo
        mediante el Algoritmo Dijkstra Mejorado. Puesto que Dijkstra devuelve un
        diccionario con los padres de cada vértices con items (objeto_vertice:
        objeto_vertice), deberemos inferir de este resultado general el camino
        local entre origen y destino. Para ello, recorreremos de manera inversa
        los padres, partiendo del destino y llegando al origen

        Args: origen vértice del grafo de origen
              destino vértice del grafo de destino

        Returns: Devuelve una tupla cuyos elementos son una lista con los
        vértices a visitar (en orden) y el coste total de este camino. Si no existe el camino desde origen hasta destino, devuelve (None, None)
        '''
        # Vamos al padre de cada vertice hasta llegar al origen

        padre = self.dijkstra_mejorado(origen, destino)
        # Sacamos djikistra desde el origen

        if destino not in padre.keys():
            return (None, None)
        else:

            coste = 0
            camino = [destino]
            actual = destino
            # Vamos recorriendo el árbol de caminos mínimos hasta llegar al origen
            while actual != origen:
                proximo = padre[actual]
                camino.append(proximo)
                coste += self.obtener_arista(actual, proximo)[1]
                actual = proximo

            return (camino[::-1], coste)

    def dijkstra_mejorado(self, origen, destino):
        """ Calcula un Árbol Abarcador Mínimo para el grafo partiendo
        del vértice "origen" usando el algoritmo de Dijkstra.
        Calcula únicamente el árbol de la componente
        conexa que contiene a "origen". Además, si llega al vértice de destino, se para.

        Args: origen vértice del grafo de origen
        Returns: Devuelve un diccionario que indica,
        para cada vértice alcanzable desde "origen",
        qué vértice es su padre en el árbol abarcador mínimo.
        """

        # Igual que djikstra pero con condición de parada

        padre, visitado, dist = {}, {}, {}
        for vertex in list(self.vertices.keys()):
            # Inicializamos padres, vértices y visitados
            # de cada vértice usando diccionarios
            padre[vertex] = None
            visitado[vertex] = False
            dist[vertex] = INFTY

        dist[origen] = 0  # Del origen al origen, no hay distancia
        i = 0
        Q = [(dist[origen], i, origen)]
        i += 1

        # Lista de prioridad ordenada por d
        while visitado[destino] == False and len(Q):

            # Extraemos el elemento v con menor distancia de Q

            v = heapq.heappop(Q)[2]

            # Con lo programado en las 3 líneas anteriores, queremos saber
            # cuál es el par (clave, valor) que debemos borrar (aquel que
            # tiene el mayor valor de distancia)

            if not visitado[v]:
                visitado[v] = True
                for w in self.vertices[v].adyacencia:
                    # Si no hemos visitado el vertice, comprobamos las distancias a los otros vertices adyacentes
                    arista = self.obtener_arista(v, w)
                    # Se compara con la que tenemos hasta el momento + esa arista
                    # Si es menor se cambia y añade a la lista de prioridad
                    if dist[v] + arista[1] < dist[w]:
                        dist[w] = dist[v] + arista[1]
                        padre[w] = v
                        heapq.heappush(
                            Q, (dist[w], i, w))
                        i += 1

        return padre


if __name__ == "__main__":
    pass
