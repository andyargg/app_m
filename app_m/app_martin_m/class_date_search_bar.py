import flet as ft



class DateSearchBar(ft.UserControl):
    def __init__(self):
        self.obj = None
        super().__init__()

    def open_anchor(self,e):
        self.obj.open_view()
        
    def close_anchor(self,e):
        if not e.control.data:
            text = f"{e.control.data}"
        else:
            text = ""
       
        self.obj.close_view(text)
    
    def change_item(self,e):
        print(f"{e.data}")
        
    def create_search_bar(self):
        anchor = ft.SearchBar(
            width=450,
            bar_bgcolor="#FFFFFF",
            view_bgcolor="#FFFFFF",
            value="",
            view_elevation=4,
            bar_hint_text=f"Busca por fecha",
            bar_leading=ft.IconButton(icon="search", on_click=self.open_anchor,icon_color=ft.colors.SECONDARY),
            on_change=self.change_item,
            view_trailing=
            [
                ft.IconButton(icon="close",on_click=self.close_anchor,icon_color=ft.colors.SECONDARY),
            ],
        )

        self.obj = anchor
        return anchor

    def build(self):
        return self.create_search_bar()

# def main(page):
#     sbar = DateSearchBar(page)
#     page.add(sbar.build())
    


# ft.app(target=main)