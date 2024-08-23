import flet as ft
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

martindb = credentials.Certificate('firebase_config.json')
firebase_admin.initialize_app(martindb, {
    'databaseURL': 'https://martindb-2d220-default-rtdb.firebaseio.com/',
    
}, name="searchBar")

class MySearchBar(ft.UserControl):
    def __init__(self, data_received):
        self.data_received = data_received
        self.obj = None
        super().__init__()

    def open_anchor(self, e):
        self.obj.open_view()

    def close_anchor(self, e):
        if e.control.data is not None:
            text = f"{e.control.data}"
        else:
            text = ""

        self.obj.close_view(text)

    def fetch_data(self):
        ref = db.reference('/', app=firebase_admin.get_app("searchBar"))
        try:
            snapshot = ref.get()

            output_list = []
            if isinstance(snapshot, list):  # Si la raíz es una lista
                for value in snapshot:
                    if self.data_received == "Patentes" and 'Patente' in value:
                        output_list.append(value['Patente'])
                    elif self.data_received == "Tecnico" and 'Tecnico' in value:
                        output_list.append(value['Tecnico'])
           
            return output_list
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []  # Retorna una lista vacía en caso de error

    def print_data(self):
        print(self.result())
    

    def create_search_bar(self):
        anchor = ft.SearchBar(
            width=450,
            bar_bgcolor="#383763",
            view_bgcolor="#383763",
            value="",
            view_elevation=4,
            bar_hint_text=f"Busca {self.data_received}...",
            view_hint_text=f"Busca {self.data_received}...",
            bar_leading=ft.IconButton(icon="search", on_click=self.open_anchor, icon_color=ft.colors.SECONDARY),
            on_tap=self.open_anchor,
            
            
            view_trailing=[
                ft.IconButton(icon="close",on_click=self.close_anchor),
            ],

            controls=[
               ft.ListTile(
                   title=ft.Text(f"{element}"), on_click=self.close_anchor, data=element
               )
               for element in (self.fetch_data())
            ],
        )

        self.obj = anchor
        return anchor


    def build(self):
        return self.create_search_bar()
    
# Ejemplo de uso
def main(page: ft.Page):
    page.add(MySearchBar(data_received="Patentes"))
    page.add(MySearchBar(data_received="Tecnico"))
    

ft.app(target=main)
