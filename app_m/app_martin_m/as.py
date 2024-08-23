import flet as ft

def main(page: ft.Page):

    data = [
        ["Juan", "25", "Buenos Aires"],
        ["María", "30", "Córdoba"],
        ["Pedro", "22", "Rosario"]
    ]

    expanded_row = None

    def row_clicked(e, index):
        nonlocal expanded_row
        if expanded_row == index:
            expanded_row = None  # Colapsar si se hace clic de nuevo
        else:
            expanded_row = index  # Expandir la fila clickeada
        update_table()

    def create_row(row, index):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(row[0])),
                ft.DataCell(ft.Text(row[1])),
                ft.DataCell(ft.Text(row[2])),
            ],
            on_select_changed=lambda e: row_clicked(e, index),
        )

    def create_expanded_row():
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Container(
                    content=ft.Text("Hola"),
                    padding=10,
                    bgcolor=ft.colors.RED,
                )),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text(""))
            ]
        )

    def update_table():
        rows = []
        for index, row in enumerate(data):
            rows.append(create_row(row, index))
            if expanded_row == index:
                rows.append(create_expanded_row())
        dt.rows = rows
        page.update()

    dt = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Nombre")),
            ft.DataColumn(label=ft.Text("Edad")),
            ft.DataColumn(label=ft.Text("Ciudad")),
        ],
        rows=[],  # Inicialmente vacío, se llena con update_table
        border_radius=5,
    )

    page.add(dt)
    update_table()  # Llenar la tabla inicialmente

ft.app(target=main)
