import flet as ft
from class_calendar import MyCalendar  # Import the MyCalendar class
import json

class Date:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.page.theme_mode=ft.ThemeMode.DARK
        self.page.window_width=500
        self.page.window_min_height=200
        self.page.window_max_height=700
        self.error_text=ft.Container(
            content=ft.Text(
                color=ft.colors.RED,
                size=20
            )
        )
       
    
    def save_date(self,e,date):
        
        try:    
            data={"date":date}

            file_name="date.json"

            with open(file_name, "w",encoding='utf-8') as json_file:
                json.dump(data, json_file,ensure_ascii=False,indent=4)
        except Exception as e:
            print(f"Error: {e}")

    
    def go_next(self,e):
        if not self.calendar.output.content.value:
            self.error_text.content.value="Elige la fecha primero"
            self.error_text.update()
            print("No entra")
        else:
            print("Entra")
            self.error_text.content.value=""
            self.error_text.update()
            self.save_date(e,self.calendar.output.content.value)
            self.page.go("/form")

    def create_date_ui(self):
        # Create an instance of MyCalendar
        self.calendar=MyCalendar()
        my_calendar = ft.Container(
            padding=15,
            margin=10,
            width=self.page.width,
            border_radius=35,
            bgcolor="#090C34",
            content=ft.Column(
                scroll=ft.ScrollMode.ALWAYS,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=50,
                controls=[
                    ft.Text(
                        "Elige la fecha para empezar",
                        size=20,
                        style=ft.TextStyle(
                            decoration=ft.TextDecoration.UNDERLINE
                        )

                    ),
                    self.calendar,
                    self.calendar.output,
                    self.error_text,
                    ft.ElevatedButton(
                   
                    text="Empezar",
                    style=ft.ButtonStyle(
                        color={
                            ft.MaterialState.DEFAULT: "#FAF8FF",
                        },
                    ),
                    bgcolor={"": "#383763"},
                    on_click=self.go_next,
                    
                    )
                ],
            )
        )

        # Add other UI components as needed
        # For example, add my_calendar to a container or column
        cal_list_view = ft.ListView(expand=1, auto_scroll=False)
        cal_list_view.controls.append(my_calendar)

        return cal_list_view
        # Return the root UI control
        return my_calendar  # Modify this based on your UI structure
    def build(self):
        # Call create_date_ui to build the UI
        return self.create_date_ui()

# def main(page: ft.Page):
#     init = Date(page)
#     # Add application's root control to the page
#     page.add(init.build())

# ft.app(target=main)
