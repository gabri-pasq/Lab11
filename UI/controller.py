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
        colori = DAO.getcolor()
        for i in colori:
            self._view._ddcolor.options.append(ft.dropdown.Option(i))


    def handle_graph(self, e):
        colore = self._view._ddcolor.value
        anno = self._view._ddyear.value
        if colore is None:
            self._view.create_alert('Inserire colore')
            return
        if anno is None:
            self._view.create_alert('Inserire anno')
            return

        self._model.creagrafo(colore)
        self._model.creaconnessioni(int(anno),colore)
        self._view.txtOut.controls.clear()


        self._view.txtOut.controls.append(ft.Text(f'Numero di vertici: {self._model.numnodi()} -- Numero di archi: {self._model.numarchi()}'))
        lista = self._model.tremaggiori()
        for i in lista:
            self._view.txtOut.controls.append(
                ft.Text(f'Arco da {i[0]} a {i[1]}, peso: {i[2]}'))


        self._view.update_page()
        self.fillDDProduct()
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