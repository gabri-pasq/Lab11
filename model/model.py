import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.nodi = []
        self.grafo = nx.Graph()
        self.idmap = {}


    def creagrafo(self, naz):
        self.nodi = DAO.getnodi(naz)
        self.grafo.add_nodes_from(self.nodi)
        for i in self.nodi:
            self.idmap[i.Retailer_code] = i

    def creaconnessioni(self, anno):
        for i in self.grafo.nodes:
            archi = DAO.getarchi(anno,i)
            for x, y, z in archi:
                if self.grafo.has_edge(self.idmap[x], self.idmap[y]):
                    continue
                else:
                    self.grafo.add_edge(self.idmap[x], self.idmap[y], weight=z)




    def numnodi(self):
        return len(self.grafo.nodes)

    def numarchi(self):
        return len(self.grafo.edges)


    def allpesi(self):
        lista=[]
        for i in self.grafo.nodes:
            vicini = self.grafo.neighbors(i)
            somma=0
            for k in vicini:
                somma += self.grafo[i][k]['weight']
            lista.append((i.Retailer_name,somma))
        ls = sorted(lista, key=lambda x: x[1], reverse=True)
        return ls