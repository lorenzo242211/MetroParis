import geopy.distance
from database.DAO import DAO
import networkx as nx
from model.connessione import Connessione

def getPeso(u, v, velocita):
    distanza = geopy.distance.distance((u.coordX, u.coordY),(v.coordX, v.coordY)).km
    tempo = distanza / velocita
    return tempo*60


class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self.grafo = nx.DiGraph()
        self.idMapFermate = {} #una semplice dizionario che associa chiave primaria ad un oggetto;
        #per recuperare un oggetto.-———__:
        for f in self._fermate:
            self.idMapFermate[f.id_fermata] = f #un semplice dizionario che contenga oggetti connessione
            #associati all'id fermata

    def buildGraph(self):
        # verifica prima che grafo sia vuoto
        self.grafo.clear()
        self.grafo.add_nodes_from(self._fermate)
        self.addedges3()

    def buildGraphPesato(self):
        self.grafo.clear()
        self.grafo.add_nodes_from(self._fermate)
        self.addEdgesPesatiTempi()

    def addEdgesPesato1(self): #alternativa farlo tranquillamente nel DAO
        #prendo spunto da addedges3
        self.grafo.clear_edges()
        alledges = DAO.getAllEdges()
        for connessione in alledges:
            u = self.idMapFermate[connessione.id_stazP]
            v = self.idMapFermate[connessione.id_stazA]
            if self.grafo.has_edge(u,v):
                self.grafo[u][v]['weight'] += 1 #se ribecco stesso arco prima scartavo ora aggiungo peso
            else:
                self.grafo.add_edge(u,v, weight=1)

    '''def addEdgesPesatoQuery(self):
        #sfrutta la query del DAO
        self.grafo.clear_edges()
        allEdgesPeso = DAO.getAllEdgesPeso()
        for tupla in allEdgesPeso:
            self.grafo.add_edge(self.idMapFermate[tupla[0]], self.idMapFermate[tupla[1]], weight=tupla[2])'''

    def addedges(self):
        for u in self._fermate:
            for v in self._fermate:
                if DAO.haconnessione(u, v):
                    self.grafo.add_edge(u, v)

    def addedges2(self):
        for u in self._fermate:
            for connessione in DAO.getvicini(u):# non è un doppio for come prima ma un ciclo per ogni nodo di partenza e trovato lui valuto i suoi vicini ovvero solo quelli a cui lui è connesso
                v = self.idMapFermate[connessione.id_stazA]
                self.grafo.add_edge(u, v)

    def addedges3(self): #quello che avrei usato io
        #terzo modo senza cicli ovvero aggiungere una connessione se e solo se esiste una connessione
        alledges = DAO.getAllEdges()
        for connessione in alledges:
            u = self.idMapFermate[connessione.id_stazP]
            v = self.idMapFermate[connessione.id_stazA]
            self.grafo.add_edge(u, v)

    def getnumnodi(self):
        return len(self.grafo.nodes())

    def getnumarchi(self):
        return len(self.grafo.edges())

#BFS per archi non pesati utile per cammino minimo
#DFS, visita in profondità, ogni step vediamo uno dei nodi vicini non visitato finchè non finisce i vicini e torno ad S


    def getBFSnodesFromEdges(self, sorgente):
        archi = nx.bfs_edges(self.grafo, sorgente)
        nodiBFS = []
        for u,v in archi:
            nodiBFS.append(v)
        return nodiBFS


    def getDFSnodesFromEdges(self, sorgente): #il metodo di esplorazione ha logica diversa
        #quindi l'ordine è completamente differente
        archi = nx.dfs_edges(self.grafo, sorgente) #restituisce un iterable di archi
        nodiDFS = []
        for u,v in archi:
            nodiDFS.append(v)
        return nodiDFS

    #metodi 2, albero di visita
    def getBFSnodesFromTree(self, sorgente): #restituisce un grafo, l'albero di visita
        tree = nx.bfs_tree(self.grafo, sorgente)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi

    def getDFSnodesFromTree(self, sorgente):
        tree = nx.dfs_tree(self.grafo, sorgente)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi

    def addEdgesPesatiTempi(self):
        #crea archi in cui il peso è pari al tempo di percorrenza di quell arco, ottenuto come rapporto tra  distanza tra 2 staz e
        #e la velocità di percorrenza
        self.grafo.clear_edges()
        alledges = DAO.getAllEdgesVeloc()
        for e in alledges:
            u = self.idMapFermate[e[0]]
            v = self.idMapFermate[e[1]]
            velocita = e[2]
            peso = getPeso(u, v , velocita) #tempo di percorrenza
            self.grafo.add_edge(u, v, weight=peso)

    def getPercorsoCorto(self, u, v):
        return nx.single_source_dijkstra(self.grafo, u, v) #restituisce peso (tempo) + sequenza nodi del cammino minimo

    @property
    def fermate(self):
        return self._fermate