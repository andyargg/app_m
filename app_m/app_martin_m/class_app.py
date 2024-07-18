import flet as ft
from class_date_search_bar import DateSearchBar

class App:
    def __init__(self,page) -> None:
        self.page = page
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 500
        self.page.window_min_height = 200
        self.page.window_max_height = 700

    def create_page_ui(self):
        app = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Bienvenido", weight="bold", size=30),
                    ft.Container(
                        border_radius=ft.border_radius.all(30),
                        border=ft.border.all(1, ft.colors.BLACK),
                        content=DateSearchBar()),
                    
                    
                ]
            )
        )

        return app

    def build(self):
        return self.create_page_ui()
        



def main(page):
    app = App(page)
    page.add(app.build())
    


ft.app(target=main)