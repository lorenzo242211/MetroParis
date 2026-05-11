import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._fermataPartenza = None
        self._fermataArrivo = None

    def handleTrovaPercorso(self, e): #trovo attraverso velocità media e dijsktra il miglior percorso e piu veloce
        #non faccio tutti gli if del cazzo passiamo subito a dijkstra
        if self._fermataPartenza and self._fermataArrivo and self._fermataArrivo.id_fermata != self._fermataPartenza.id_fermata:
            totTempo, percorso = self._model.getPercorsoCorto(self._fermataPartenza, self._fermataArrivo)
            if len(percorso) == 0:
                self._view.lst_result.controls.clear()
                self._view.lst_result.controls.append(ft.Text("Percorso non trovato", color="red"))
                self._view.update_page()
                return
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text(f"Tempo totale del percorso Dijkstra fra {self._fermataPartenza.nome} e {self._fermataArrivo.nome}: {totTempo:.2f} minuti; di seguito le fermate da prendere per arrivare a destinazione nel minor tempo possibile:", color="blue"))
            for indice, p in enumerate(percorso):
                if indice == 0:
                    self._view.lst_result.controls.append(ft.Text(f"Partenza: {p}", color="orange"))
                elif indice == len(percorso) - 1:
                    self._view.lst_result.controls.append(ft.Text(f"Arrivo: {p}", color="orange"))
                else:
                    self._view.lst_result.controls.append(ft.Text(p))

        else:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Attenzione! Errore o sei un down e partenza = arrivo, o grafo non creato correttamente / selezione errata fermata arrivo/partenza", color="red"))
        self._view.update_page()
        return


    def handleCreaGrafo(self,e):
        self._model.buildGraphPesato()
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("Grafo creato correttamente!", size=30, color="blue"))
        self._view.lst_result.controls.append(ft.Text(f"Numero nodi: {self._model.getnumnodi()} | Numero archi: {self._model.getnumarchi()}"))
        #suppongo database mysql sia ok, non metto caso non abilitazione pulsanti
        self._view._ddStazPartenza.disabled = False
        self._view._ddStazArrivo.disabled = False
        self._view._btnCalcola.disabled = False
        self._view.update_page()

    def handleCercaRaggiungibili(self,e):
        if self._fermataPartenza is None:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Attenzione! Inserire fermata di partenza.", color="red"))
            self._view.update_page()
            return
        nodi = self._model.getBFSnodesFromEdges(self._fermataPartenza)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"Data la fermata di partenza selezionata '{self._fermataPartenza.nome}', sono"
                                                      f"stati trovati {len(nodi)} nodi:" , color="blue"))
        for n in nodi:
            self._view.lst_result.controls.append(ft.Text(n))
        self._view.update_page()

    def loadFermate(self, dd: ft.Dropdown()):
        fermate = self._model.fermate

        if dd.label == "Stazione di Partenza":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Partenza))
        elif dd.label == "Stazione di Arrivo":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Arrivo))

    def read_DD_Partenza(self,e):
        print("read_DD_Partenza called ")
        if e.control.data is None:
            self._fermataPartenza = None
        else:
            self._fermataPartenza = e.control.data

    def read_DD_Arrivo(self,e):
        print("read_DD_Arrivo called ")
        if e.control.data is None:
            self._fermataArrivo = None
        else:
            self._fermataArrivo = e.control.data
