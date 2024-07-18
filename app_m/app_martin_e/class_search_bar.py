import flet as ft
from class_mysql import Database
import asyncio

class MySearchBar(ft.UserControl):
    def __init__(self,data_received):
        self.data_received = data_received
        self.result = asyncio.run(self.data())
        self.obj = None
        super().__init__()

    def open_anchor(self,e):
        self.obj.open_view()
        
    def close_anchor(self,e):
        if e.control.data != None:
            text = f"{e.control.data}"
        else:
            text = ""
       
        self.obj.close_view(text)
    
    async def data(self):
        db = Database(host="localhost", user="root", password="h1h2h39zho", database="camionetas")
        output_list = []
        query = "SELECT Patente, Tecnico FROM camionetas"
        results = await db.execute(query)
        for data in results:
            if self.data_received=="Patentes":
                output_list.append(data[0])
            elif self.data_received=="Tecnico":
                output_list.append(data[1])
          
        return (output_list)
    
    def change_item(self,e):
        print(f"{e.data}")
        
    def create_search_bar(self):
        anchor = ft.SearchBar(
            width=450,
            bar_bgcolor="#383763",
            view_bgcolor="#383763",
            value="",
            view_elevation=4,
            bar_hint_text=f"Busca {self.data_received}...",
            view_hint_text=f"Busca {self.data_received}...",
            bar_leading=ft.IconButton(icon="search", on_click=self.open_anchor,icon_color=ft.colors.SECONDARY),
            on_change=self.change_item,
            view_trailing=[
                ft.IconButton(icon="close",on_click=self.close_anchor,icon_color=ft.colors.SECONDARY),
            ],

            controls=[
               ft.ListTile(
                   title=ft.Text(f"{element}"), on_click=self.close_anchor, data=element
               )
               for element in (self.result)
            ],
        )

        self.obj = anchor
        return anchor

    def build(self):
        return self.create_search_bar()

