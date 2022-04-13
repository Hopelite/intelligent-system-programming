from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.actionbar import ActionBar
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from src.persistence.models import ViewAppointment

class TableScreen(Screen):
    def __init__(self, appointments: list[ViewAppointment], **kw):
        super().__init__(**kw)
        self.add_widget(Table(appointments))
        self.add_widget(TableScreenActionBar())

class ProgramScreenManager(ScreenManager):
    def __init__(self, table_screen: TableScreen) -> None:
        super().__init__()
        self.add_widget(table_screen)
        self.add_widget(SearchScreen(name='search_screen'))
        self.add_widget(DeleteScreen(name='delete_screen'))

class ScreenLayout(Screen):
    pass

class TableScreenActionBar(ActionBar):
    def get_search_screen(self):
        return SearchScreen()

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
        self.add_widget(TableCell(text=appointment.patient_date_of_birth.strftime('%m-%d-%Y')))
        self.add_widget(TableCell(text=appointment.appointent_date.strftime('%m-%d-%Y')))
        self.add_widget(TableCell(text=appointment.doctor_name))
        self.add_widget(TableCell(text=appointment.conclusion))

    def __build_empty_row(self):
        for col in range(self.cols):
            self.add_widget(TableCell(text=''))

class MoreDataThenRowsException(Exception):
    pass

class TableCell(Label):
    pass

class SearchScreen(Screen):
    pass

class AddScreen(Screen):
    pass
    
class DeleteScreen(Screen):
    pass