
from class_form import Form
from class_date import Date
import flet as ft

def main(page: ft.Page):
    page.title = "Routes Example"
    
    date = Date(page)
    form = Form(page)

    def route_change(route):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        date.build()
                    ],
                )
            )
        if page.route == "/form":
            page.views.append(
                ft.View(
                    "/form",
                    [
                        form.build()
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

