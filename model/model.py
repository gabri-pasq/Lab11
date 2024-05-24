import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.nodi = []
        self.grafo = nx.Graph()
        self.idmap = {}
        self.percorsofinale = []
        self.lunghezzaarchi = 0
        self.peso = 0
        self.fine = False

    def creagrafo(self, colore):
        self.nodi = DAO.getnodi(colore)
        self.grafo.add_nodes_from(self.nodi)
        for i in self.nodi:
            self.idmap[i.Product_number] = i

    def creaconnessioni(self, anno, colore):
        archi = DAO.getarchi(anno, colore)
        for x, y, z in archi:
            if self.grafo.has_edge(x, y):
                continue
            else:
                self.grafo.add_edge(self.idmap[x], self.idmap[y], weight=z)

    def percorso(self, id):
        self.lunghezzaarchi = 0

        self.fine = False
        self.percorsofinale = []
        nodo = self.idmap[id]

        print(len(nx.dfs_tree(self.grafo)))
        print(nx.dfs_tree(self.grafo))
        self.ricorsione([nodo], [])
        return self.percorsofinale, self.lunghezzaarchi

    def ricorsione(self, parziale, archiParziale):
        for v in self.grafo.neighbors(parziale[-1]):
            if (v, parziale[-1]) not in archiParziale and (parziale[-1], v) not in archiParziale:
                parziale.append(v)
                archiParziale.append((parziale[-2], parziale[-1]))
                self.ricorsione(parziale, archiParziale)
                parziale.pop()
                archiParziale.pop()
            else:
                if self.check(parziale):
                    if self.lunghezzaarchi < len(archiParziale):
                        self.lunghezzaarchi = len(archiParziale)
                        self.percorsofinale = copy.deepcopy(parziale)

    def check(self, lista):
        peso = 0
        for i in range(0, len(lista) - 1):
            if self.grafo[lista[i]][lista[i + 1]]['weight'] > peso:
                peso = self.grafo[lista[i]][lista[i + 1]]['weight']
            else:
                return False
        return True

    def numnodi(self):
        return len(self.grafo.nodes)

    def numarchi(self):
        return len(self.grafo.edges)

    def tremaggiori(self):
        l = []
        for u, v in self.grafo.edges:
            l.append((u, v, self.grafo[u][v]['weight']))
        fine = sorted(l, key=lambda x: x[2], reverse=True)
        return fine[:3]
