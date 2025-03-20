import heapq as heapq

class GraphRoutes:

    def __init__(self, graphosmnx):

        self.graph_dict = {}
        self.node_coords = {}

        for u, v, data in graphosmnx.edges(data=True):
            if u not in self.graph_dict:
                self.graph_dict[u] = []

            if (v, data['length']) not in self.graph_dict[u]:
                self.graph_dict[u].append((v, data['length']))

            if not data.get('oneway', False):
                if v not in self.graph_dict:
                    self.graph_dict[v] = []

                if (u, data['length']) not in self.graph_dict[v]:
                    self.graph_dict[v].append((u, data['length']))


        for node, data in graphosmnx.nodes(data=True):
            self.node_coords[node] = [data['y'], data['x']]


    def showGraph(self):
       return self.graph_dict
        

    def dijkstra(self, inicio, destino):
      distancias = {nodo: float('inf') for nodo in self.graph_dict}
      distancias[inicio] = 0
      
      cola = [(0, inicio)]
      padres = {inicio: None} 

      while cola:
          distancia_actual, nodo_actual = heapq.heappop(cola)

          if nodo_actual == destino:
              break

          for vecino, peso in self.graph_dict[nodo_actual]:
              distancia = distancia_actual + peso

              if distancia < distancias[vecino]:
                  distancias[vecino] = distancia
                  padres[vecino] = nodo_actual
                  heapq.heappush(cola, (distancia, vecino))

      camino = []
      nodo = destino
      while nodo is not None:
          camino.append(self.node_coords[nodo])
          nodo = padres[nodo]
      camino.reverse()

      return camino, distancias[destino]