import flet as ft
from class_search_bar import MySearchBar
import json
import os
import atexit
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

informacion_camionetas = credentials.Certificate('firebase_config.json')
firebase_admin.initialize_app(informacion_camionetas, {
    'databaseURL': 'https://informacioncamionetas-44aae-default-rtdb.firebaseio.com/',
    }, name="formulario")


class Form:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window.width = 500
        self.page.window.min_height = 200
        self.page.window.max_height = 700
        self.txt_number = ft.Text("1", size=15)
        self.send_button = ft.ElevatedButton(visible=False)
        self.data_list = []
        atexit.register(self.delete_json)

    def button_next_clicked(self):
        self.txt_number.value = str(int(self.txt_number.value) + 1)
        self.page.update()

    def button_back_clicked(self, e):
        if self.txt_number.value == "1":
            self.txt_number.value = "1"
        else:
            self.txt_number.value = str(int(self.txt_number.value) - 1)
            self.load_data_json("data.json")

        self.page.update()

    def upload_truck_data(
            plate,
            technician,
            order,
            cleaning,
            water,
            spare_tire,
            oil,
            jack,
            cross_wrench,
            fire_extinguisher,
            padlock,
            comment
        ):
        try:
            ref = db.reference('/', app=informacion_camionetas)

            new_truck_key = ref.push().key

            data = {
                'Patente': plate,
                'Tecnico': technician,
                'Orden': order,
                'Limpieza': cleaning,
                'Agua': water,
                'Rueda_de_auxilio': spare_tire,
                'Aceite': oil,
                'Crique': jack,
                'Llave_cruz': cross_wrench,
                'Matafuego': fire_extinguisher,
                'Candado': padlock,
                'Comentario': comment
            }

            # Upload the data to Firebase
            ref.child(new_truck_key).set(data)

            print(f"Datos subidos exitosamente a la base de datos con la clave: {new_truck_key}")

        except Exception as e:
            print(f"Error al subir los datos a la base de datos: {str(e)}")


    def validate_form(self, e):
        flag_1 = True
        flag_2 = True
        for dropdown in self.dropdowns:
            if not dropdown.value:
                dropdown.error_text = "Selecciona una opcion"
                flag_1 = False
                dropdown.update()
            else:
                dropdown.error_text = ""
                dropdown.update()

        for search_boxes in self.search_bars:
            if not search_boxes.controls[0].value:
                search_boxes.obj.bar_bgcolor = "#9B1008"
                search_boxes.obj.bar_hint_text = "Completa esta casilla"
                flag_2 = False
            else:
                search_boxes.obj.bar_bgcolor = "#383763"
            search_boxes.obj.update()

        if flag_1 and flag_2:
            self.upload_data_json(
                self.search_bars[0].obj.value,
                self.search_bars[1].obj.value,
                self.dropdowns[0].value,
                self.dropdowns[1].value,
                self.dropdowns[2].value,
                self.dropdowns[3].value,
                self.dropdowns[4].value,
                self.dropdowns[5].value,
                self.dropdowns[6].value,
                self.dropdowns[7].value,
                self.dropdowns[8].value,
                self.container.content.controls[1].controls[11].value
            )

            self.search_bars[0].obj.value = "Patentes"
            self.search_bars[1].obj.value = "Técnicos"
            self.search_bars[0].obj.update()
            self.search_bars[1].obj.update()

            self.ui_send_button()

            self.button_next_clicked()
            for dropdown in self.dropdowns:
                dropdown.value = ""

        self.page.update()

    def send_form(self, e):
        self.upload_truck_data(
            self.container.content.controls[1].controls[0].controls[0].value,  # searchbar 1
            self.container.content.controls[1].controls[1].controls[0].value,  # searchbar 2
            self.container.content.controls[1].controls[2].value,  # Orden
            self.container.content.controls[1].controls[3].value,  # Limpieza
            self.container.content.controls[1].controls[4].value,  # Agua
            self.container.content.controls[1].controls[5].value,  # Rueda
            self.container.content.controls[1].controls[6].value,  # Aceite
            self.container.content.controls[1].controls[7].value,  # Crique
            self.container.content.controls[1].controls[8].value,  # Llave Cruz
            self.container.content.controls[1].controls[9].value,  # Matafuego
            self.container.content.controls[1].controls[10].value,  # Candado
            self.container.content.controls[1].controls[11].value  # Comentario
        )

        self.page.update()

    def ui_send_button(self):
        if int(self.txt_number.value) >= 3:
            self.send_button.visible = True
            self.send_button.text = "Enviar"
            self.send_button.on_click = self.send_form

    def upload_data_json(self, plate, technician, order, cleaning, water, spare_tire, oil, jack, cross_wrench, fire_extinguisher, padlock, comment):
        new_data = {
            "plate": plate,
            "technician": technician,
            "order": order,
            "cleaning": cleaning,
            "water": water,
            "spare_tire": spare_tire,
            "oil": oil,
            "jack": jack,
            "cross_wrench": cross_wrench,
            "fire_extinguisher": fire_extinguisher,
            "padlock": padlock,
            "comment": comment,
        }
        self.data_list.append(new_data)
        with open("data.json", "w") as json_file:
            json.dump(self.data_list, json_file, indent=4)

    def delete_json(self):
        if os.path.exists("data.json"):
            os.remove("data.json")
        if os.path.exists("date.json"):
            os.remove("date.json")

    def load_data_json(self, data_json):
        try:
            with open(data_json, "r") as archivo:
                form_data = json.load(archivo)

        except Exception as e:
            print(f"El archivo '{data_json}' no existe.")

        index = int(self.txt_number.value) - 1
        self.set_data_form(
            form_data[index]["plate"],
            form_data[index]["technician"],
            form_data[index]["order"],
            form_data[index]["cleaning"],
            form_data[index]["water"],
            form_data[index]["spare_tire"],
            form_data[index]["oil"],
            form_data[index]["jack"],
            form_data[index]["cross_wrench"],
            form_data[index]["fire_extinguisher"],
            form_data[index]["padlock"],
            form_data[index]["comment"],
        )

    def set_data_form(self, plate, technician, order, cleaning, water, spare_tire, oil, jack, cross_wrench, fire_extinguisher, padlock, comment):
        self.container.content.controls[1].controls[0].controls[0].value = plate  # searchbar 1
        self.container.content.controls[1].controls[1].controls[0].value = technician  # searchbar 2
        self.container.content.controls[1].controls[2].value = order  # Orden
        self.container.content.controls[1].controls[3].value = cleaning  # Limpieza
        self.container.content.controls[1].controls[4].value = water  # Agua
        self.container.content.controls[1].controls[5].value = spare_tire  # Rueda
        self.container.content.controls[1].controls[6].value = oil  # Aceite
        self.container.content.controls[1].controls[7].value = jack  # Crique
        self.container.content.controls[1].controls[8].value = cross_wrench  # Llave Cruz
        self.container.content.controls[1].controls[9].value = fire_extinguisher  # Matafuego
        self.container.content.controls[1].controls[10].value = padlock  # Candado
        self.container.content.controls[1].controls[11].value = comment  # Comentario

            

    def create_ui(self):
        self.container=ft.Container(
            margin=20,
            width=self.page.width,
            border_radius=35,
            bgcolor="#090C34",
            padding=ft.padding.only(top=30, bottom=30,left=8),
            content=ft.Column(
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Container(
                                height=30,
                                content=ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon_size=15,
                                            icon=ft.icons.ARROW_BACK_IOS_NEW_SHARP,
                                            on_click=lambda _:self.page.go("/"),
                                            bgcolor="#383763",
                                            icon_color=ft.colors.SECONDARY
                                            
                                        )
                                    ],
                                )
                            ),
                            ft.Container(
                                bgcolor="#383763",
                                margin=10,
                                border_radius=5,
                                width=130,
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("Camioneta:",size=15,),
                                        self.txt_number,
                                    ],
                                )
                            ),
                        ]
                    ),
                    ft.Column(
                        controls=[
                            MySearchBar("Patentes"),#0
                            MySearchBar("Tecnico"),#1
                            ft.Dropdown(#2
                                bgcolor="#383763",
                                border_radius=20,
                                label="Orden",
                                width=450,
                                options=[
                                    ft.dropdown.Option("Muy desordenado"),
                                    ft.dropdown.Option("Desordenado"),
                                    ft.dropdown.Option("Ordenado"),
                                    ft.dropdown.Option("Muy ordenado"),
                                ]
                            ),
                            ft.Dropdown(#3
                                bgcolor="#383763",
                                label="Limpieza",
                                border_radius=20,
                                width=450,
                                options=[
                                    ft.dropdown.Option("Muy sucio"),
                                    ft.dropdown.Option("Sucio"),
                                    ft.dropdown.Option("Limpio"),
                                    ft.dropdown.Option("Muy limpio"),
                                ]
                            ),
                            ft.Dropdown(#4
                                bgcolor="#383763",
                                label="Agua",
                                width=450,
                                border_radius=20,
                                options=[
                                    ft.dropdown.Option("Si"),
                                    ft.dropdown.Option("No")
                                ]
                            ),
                            ft.Dropdown(#5
                                bgcolor="#383763",
                                label="Rueda de auxilio",
                                border_radius=20,
                                width=450,
                                options=[
                                    ft.dropdown.Option("Si"),
                                    ft.dropdown.Option("No")
                                ]
                            ),
                             ft.Dropdown(#6
                                bgcolor="#383763",
                                label="Aceite",
                                border_radius=20,
                                width=450,
                                options=[
                                    ft.dropdown.Option("Si"),
                                    ft.dropdown.Option("No")
                                ]
                            ),
                             ft.Dropdown(#7
                                bgcolor="#383763",
                                label="Crique",
                                border_radius=20,
                                width=450,
                                options=[
                                    ft.dropdown.Option("Si"),
                                    ft.dropdown.Option("No")
                                ]
                            ),
                            ft.Dropdown(#8
                                bgcolor="#383763",
                                label="Llave cruz",
                                border_radius=20,
                                width=450,
                                options=[
                                    ft.dropdown.Option("Si"),
                                    ft.dropdown.Option("No")
                                ]
                            ),
                            ft.Dropdown(#9
                            bgcolor="#383763",
                            label="Matafuego",
                            border_radius=20,
                            width=450,
                            options=[
                                ft.dropdown.Option("Si"),
                                ft.dropdown.Option("No")
                            ]
                        ),
                            ft.Dropdown(#10
                            bgcolor="#383763",
                            label="Candado",
                            border_radius=20,
                            width=450,
                            options=[
                                ft.dropdown.Option("Si"),
                                ft.dropdown.Option("No")
                            ]
                        ),
                            ft.TextField(#11
                                bgcolor="#383763",
                                label="Deja un comentario",
                                width=450,
                                border_radius=20,

                            ),
                            ft.Row(#
                            controls=[
                                ft.ElevatedButton(
                                    bgcolor="#383763",
                                    text="Anterior",
                                    on_click=self.button_back_clicked
                                ),
                                self.send_button,
                                ft.ElevatedButton(
                                    bgcolor="#383763",
                                    text="Siguiente",
                                    on_click=self.validate_form
                                ),

                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                    ]
                ),
            ]
        )
    )

        

       
        self.dropdowns = [
            self.container.content.controls[1].controls[2],#Orden
            self.container.content.controls[1].controls[3],#Limpieza
            self.container.content.controls[1].controls[4],#Agua
            self.container.content.controls[1].controls[5],#Rueda
            self.container.content.controls[1].controls[6],#Aceite
            self.container.content.controls[1].controls[7],#Crique
            self.container.content.controls[1].controls[8],#Llave Cruz
            self.container.content.controls[1].controls[9],#Matafuego
            self.container.content.controls[1].controls[10],#Candado
        ]
        self.search_bars = [
            self.container.content.controls[1].controls[0],#searchbar 1
            self.container.content.controls[1].controls[1],#searchbar 2
        ]



        self.list_view = ft.ListView(expand=1, auto_scroll=False)
        self.list_view.controls.append(self.container)

        return self.list_view

    def build(self):
        return self.create_ui()

def main(page):
    form = Form(page)
    page.add(form.build())
    


ft.app(target=main)