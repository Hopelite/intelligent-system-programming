from datetime import date
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout
from models import ViewAppointment

class ScreenLayout(Screen):
    pass

class LayoutActionBar(ActionBar):
    pass

class TableScreen(ScreenLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        table = Table([ViewAppointment("V", "V", date(2020,1,1), date(2020,1,1), 'V', 'V')])
        self.add_widget(table)

class Table(BoxLayout):
    '''Represents appointments table.'''
    def __init__(self, appointments: list[ViewAppointment], **kwargs):
        super().__init__(**kwargs)
        self.__build_table(appointments)

    def __build_table(self, appointments: list[ViewAppointment]) -> None:
        for appointment in appointments:
            self.add_widget(TableRow(appointment))

class TableRow(BoxLayout):
    '''Represents table row with one appointment.'''
    def __init__(self, appointment: ViewAppointment, **kwargs):
        super().__init__(**kwargs)
        self.__build_table_row(appointment)

    def __build_table_row(self, appointment: ViewAppointment) -> None:
        self.add_widget(TableCell(text=appointment.patient_name))
        self.add_widget(TableCell(text=appointment.patient_address))
        self.add_widget(TableCell(text=appointment.patient_date_of_birth.__str__()))
        self.add_widget(TableCell(text=appointment.appointent_date.__str__()))
        self.add_widget(TableCell(text=appointment.doctor_name))
        self.add_widget(TableCell(text=appointment.conclusion))

class TableCell(Label):
    pass