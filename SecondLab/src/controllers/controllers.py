from datetime import date
from src.persistence.models import ViewAppointment
from src.persistence.data_storage import InMemoryStorage
from src.persistence.repository import Repository
from src.views.views import ProgramScreenManager, TableScreen

class ViewAppointmentsController:
    def __init__(self) -> None:
        appointments = [ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'),
         ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'),
          ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'),
           ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'),
            ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'),
             ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'),
              ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'),
               ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'),
                ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'),
                 ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'),
                  ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'),
                   ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'),
                    ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'),
                     ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me'),
                      ViewAppointment('Vadim', 'Minsk', date(2003, 2, 12), date(2022, 2, 12), 'Dr. Who', 'Help me')]
        storage = InMemoryStorage[list[ViewAppointment]](appointments)
        self._repository = Repository[ViewAppointment](storage)

    def start_program(self) -> ProgramScreenManager:
        table_screen = self.get_table()
        return ProgramScreenManager(table_screen) 

    def get_table(self, page: int = 1, size: int = 10) -> TableScreen:
        appointments = self._repository.get_all()[(page - 1) * size:size]
        return TableScreen(appointments)