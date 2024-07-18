import flet as ft

def main(page: ft.Page):
    page.title = "Animación de expansión de cuadrados"
    
    # Definimos las propiedades de los cuadrados
    expanded_height = 200  # Altura expandida del cuadrado superior
    collapsed_height = 100  # Altura colapsada del cuadrado superior
    square_color = ft.colors.BLUE  # Color del cuadrado superior
    lower_square_color = ft.colors.GREEN  # Color del cuadrado inferior

    # Creamos los cuadrados con sus alturas iniciales
    upper_square = ft.Container(
        width=300,
        height=collapsed_height,
        bgcolor=square_color,
        alignment=ft.alignment.center,
        animate_size=500  # Animación de tamaño
    )

    lower_square = ft.Container(
        width=300,
        height=100,
        bgcolor=lower_square_color,
        alignment=ft.alignment.center,
    )

    # Función que se ejecuta al hacer clic en el cuadrado superior
    def expand_upper_square(e):
        new_height = expanded_height if upper_square.height == collapsed_height else collapsed_height
        upper_square.height = new_height
        upper_square.update()

    # Añadimos el evento de clic al cuadrado superior
    upper_square.on_click = expand_upper_square

    # Agregamos los cuadrados al layout de la página
    page.add(
        ft.Column(
            controls=[
                upper_square,
                lower_square
            ],
            alignment=ft.MainAxisAlignment.start,
        )
    )

# Ejecutamos la aplicación Flet
ft.app(target=main)
