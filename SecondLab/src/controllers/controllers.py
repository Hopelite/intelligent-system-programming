from src.persistence.data_storage import XMLStorage
from src.persistence.models import ViewAppointment
from src.persistence.repository import Repository
from src.views.views import ProgramScreenManager, TableScreen

class ViewAppointmentsController:
    def __init__(self) -> None:
        storage = XMLStorage("C:\\Users\\Vadzim_Kurdzesau\\source\\repos\\BSUIR\\intelligent-system-programming\\SecondLab\\src\\input.xml")
        self._repository = Repository[ViewAppointment](storage)

    def start_program(self) -> ProgramScreenManager:
        table_screen = self.get_table()
        return ProgramScreenManager(table_screen) 

    def get_table(self, page: int = 1, size: int = 10) -> TableScreen:
        appointments = self._repository.get_all()[(page - 1) * size:size]
        return TableScreen(appointments)