from datetime import date
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.actionbar import ActionBar
from kivy.uix.gridlayout import GridLayout
from models import ViewAppointment

class ScreenLayout(Screen):
    pass

class LayoutActionBar(ActionBar):
    pass

class TableScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        appointments = [ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'), ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'), ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'), ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'), ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'), ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'), ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'), ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me')]
        self.add_widget(Table(appointments=appointments))
        self.add_widget(LayoutActionBar())

class Table(GridLayout):
    def __init__(self, appointments: list[ViewAppointment], **kwargs):
        super().__init__(**kwargs)
        number_of_appointments = len(appointments)
        if number_of_appointments > self.rows - 1:
            raise MoreDataThenRowsException("More rows than available have passed to the table.")

        self.__build_table(appointments)
        rows_left = self.rows - 1 - number_of_appointments
        for x in range(rows_left):
            self.__build_empty_row()
        
    def __build_table(self, appointments: list[ViewAppointment]) -> None:
        for appointment in appointments:
            self.__build_table_row(appointment)

    def __build_table_row(self, appointment: ViewAppointment) -> None:
        self.add_widget(TableCell(text=appointment.patient_name))
        self.add_widget(TableCell(text=appointment.patient_address))
        self.add_widget(TableCell(text=appointment.patient_date_of_birth.__str__()))
        self.add_widget(TableCell(text=appointment.appointent_date.__str__()))
        self.add_widget(TableCell(text=appointment.doctor_name))
        self.add_widget(TableCell(text=appointment.conclusion))

    def __build_empty_row(self):
        for col in range(self.cols):
            self.add_widget(TableCell(text=''))

class MoreDataThenRowsException(Exception):
    pass

class TableCell(Label):
    pass