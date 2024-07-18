
from class_datatables import DetailedDatatable
import flet as ft

def main(page: ft.Page):
    page.title = "Routes Example"
    
    datatable = DetailedDatatable(page)
    

    def route_change(route):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        datatable.build()
                    ],
                )
            )
        
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)

