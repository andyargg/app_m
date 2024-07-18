import flet as ft

class DetailedDatatable:
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
                    
                ]
            )
        )

        return app

    def build(self):
        return self.create_page_ui()
        



def main(page):
    datatable = DetailedDatatable(page)
    page.add(datatable.build())
    


ft.app(target=main)