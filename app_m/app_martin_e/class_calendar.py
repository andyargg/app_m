import flet as ft
import datetime
from calendar import HTMLCalendar
from dateutil import relativedelta
import json


class MyCalendar(ft.UserControl):
    
    def __init__(self):
        super().__init__()
        self.get_current_date()
        self.set_theme()
        # Init the container control.
        self.calendar_container = ft.Container(
            
            width=370,
            height=350,
            border=ft.border.all(5, self.border_color),
            border_radius=ft.border_radius.all(10),
            alignment=ft.alignment.bottom_center
        )
         # Build the calendar.
        self.output = ft.Container(
            padding=ft.padding.only(top=13),
            width=365,
            height=50,
            bgcolor="#383763",
            border_radius=8,
            content=ft.Text(self.load_date(),text_align="center"),
        ) # Add output control.
        self.month_class = {
            1:"Enero",
            2:"Febrero",
            3:"Marzo",
            4:"Abril",
            5:"Mayo",
            6:"Junio",
            7:"Julio",
            8:"Agosto",
            9:"Septiembre",
            10:"Octubre",
            11:"Noviembre",
            12:"Deciembre",
        }   
    def load_date(self):
        retorno=None
        try:
            with open("date.json","r") as file:
                date = json.load(file)
                retorno=date
            date = date["date"]
        except Exception as e:
            print(f"error: {e}")
            retorno=""
        
        return retorno
            
    def get_current_date(self):
        '''Get the initial current date'''
        today = datetime.datetime.today()
        self.current_month = today.month
        self.current_day   = today.day
        self.current_year  = today.year 
    
    def selected_date(self, e):
        '''User selected date'''
        self.output.content.value = e.control.data
        self.output.content.value = '/'.join(map(str,self.output.content.value))
        self.output.update()
        self.highlight_date(e)
        
            
       
        
   
        
        #return e.control.data
        
    def set_current_date(self):
        '''Set the calendar to the current date.'''
        today = datetime.datetime.today()
        self.current_month = today.month
        self.current_day   = today.day
        self.current_year  = today.year 
        self.build()
        self.calendar_container.update()
        
    def get_next(self, e):
        '''Move to the next month.'''
        current = datetime.date(self.current_year, self.current_month, self.current_day) 
        add_month = relativedelta.relativedelta(months=1)
        next_month = current + add_month
       
        self.current_year = next_month.year
        self.current_month = next_month.month
        self.current_day = next_month.day
        self.build()
        self.calendar_container.update()
    
    def get_prev(self, e):
        '''Move to the previous month.'''
        current = datetime.date(self.current_year, self.current_month, self.current_day) 
        add_month = relativedelta.relativedelta(months=1)
        next_month = current - add_month
        self.current_year = next_month.year
        self.current_month = next_month.month
        self.current_day = next_month.day
        self.build()
        self.calendar_container.update()
        
    def get_calendar(self):
        '''Get the calendar from the calendar module.'''
        cal = HTMLCalendar()
        return cal.monthdayscalendar(self.current_year, self.current_month)
    
    def set_theme(self,
                border_color="#383763", 
                text_color="#383763", 
                
            ):
        

        self.border_color = border_color
        self.text_color = text_color
    
    def highlight_date(self,e):
       
        
        if e.data == 'true':
            
            e.control.bgcolor='white10'
            e.control.update()
        else:
            e.control.bgcolor='#383763'
            e.control.update()
    
                
        
    
    def create__ui(self):
        '''Build the calendar for flet.'''
        current_calendar = self.get_calendar()
        
        str_date = f'{self.month_class[self.current_month]} {self.current_day}, {self.current_year}'
        
        date_display = ft.Text(str_date,
            
            size=20,
            color="#FAF8FF"
        )

        next_button = ft.Container(
            ft.IconButton(
                "chevron_right",
                # size=20,
                # color=self.text_color,
                on_click=self.get_next,
            ),
        )
        div = ft.Divider(
            height=1,
            thickness=4.0,
            color=self.border_color
        )
        
        prev_button = ft.Container(
            ft.IconButton(
                "chevron_left",
                
                # size=20,
                # color=self.text_color,
                on_click=self.get_prev,
            ),
        )
        
        calendar_column = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        prev_button,
                        date_display,
                        next_button,
                    ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY, 
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                
                expand=False
                ),
                div
            ],
            
            width=355,
            height=330,
            alignment=ft.MainAxisAlignment.START,
            expand=False
        )
        
        # Loop weeks and add row.
        for week in current_calendar:
            week_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
            # Loop days and add days to row.
            for day in week:
                if day > 0:
                    display_day = str(day)
                    if len(str(display_day)) == 1: display_day = '0%s' % display_day

                    day_button = ft.Container(
                        bgcolor="#383763",
                        border_radius=10,

                        width=40,
                        height=40,
                        alignment=ft.alignment.center,
                        on_hover=self.highlight_date,
                        on_click=self.selected_date,
                        content=
                            ft.Text(
                                str(display_day),
                                color="#FAF8FF",
                                size=20,
                            ), 
                        data=(
                                day,
                                self.current_month,
                                self.current_year
                            ), 
                    )   

                else:
                    day_button = ft.Container(
                        width=40,
                        height=40,
                        border_radius=ft.border_radius.all(10),
                        
                    )
                    
                week_row.controls.append(day_button)
                
            calendar_column.controls.append(week_row)
         
        self.calendar_container.content = calendar_column

        return self.calendar_container

    def build(self):
        return self.create__ui()
                
# def main(page: ft.Page):    
    
    

#     # Instantiate the FletCalendar class.
#     mycal = MyCalendar()
    
#     # Add to our application.
#     page.add(mycal, mycal.output)

#     page.update()
    
# ft.app(target=main)