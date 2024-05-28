import flet as ft
from database.DAO import DAO

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        nazioni = DAO.getNazioni()
        for i in nazioni:
            self._view._ddnation.options.append(ft.dropdown.Option(i))


    def handle_graph(self, e):
        nazione = self._view._ddnation.value
        anno = self._view._ddyear.value
        if nazione is None:
            self._view.create_alert('Inserire nazione')
            return
        if anno is None:
            self._view.create_alert('Inserire anno')
            return

        self._model.creagrafo(nazione)
        self._model.creaconnessioni(int(anno))
        self._view.txtOut.controls.clear()


        self._view.txtOut.controls.append(ft.Text(f'Numero di vertici: {self._model.numnodi()} -- Numero di archi: {self._model.numarchi()}'))
        lista = self._model.allpesi()
        for x,y in lista:
            self._view.txtOut.controls.append(
                ft.Text(f'{x} --> {y}'))



        self._view.update_page()
        #self.fillDDProduct()
        self._view.btn_search.disabled=False
        self._view.update_page()



    def fillDDProduct(self):
        for i in self._model.nodi:
            self._view._ddnode.options.append(ft.dropdown.Option(key=i.Product_number, text=i.Product_number))


    def handle_search(self, e):
        id = self._view._ddnode.value
        lista,archi = self._model.percorso(int(id))
        self._view.txtOut.controls.append(
            ft.Text(f'Numero archi: {archi}'))
        for i in lista:
            self._view.txtOut.controls.append(
                ft.Text(f'Nodo {i}'))
        self._view.update_page()