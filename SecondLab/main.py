from kivy.app import App
from src.controllers.controllers import ViewAppointmentsController
from src.views.views import SearchScreen, DeleteScreen
from kivy.lang import Builder

Builder.load_file("src/views/views.kv")

class Program(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = ViewAppointmentsController()
        self.screen_manager = self.controller.start_program()
        self.search_method = 'patient_name'
        self.current_page = 1

    def build(self):
        return self.screen_manager

    def previous(self):
        if self.current_page > 1:
            self.current_page -= 1

        return self.find_by(page=self.current_page)        

    def next(self):
        if self.current_page < self.controller.get_number_of_pages():
            self.current_page += 1

        return self.find_by(page=self.current_page)

    def find_by(self, input_data: str = None, page: int = 1):
        self.screen_manager.clear_widgets()
        if input_data == None:
            self.screen_manager.add_widget(self.controller.get_table(page))
        elif self.search_method == 'patient_name':
            self.screen_manager.add_widget(self.controller.find_by_patient_name(input_data, page))
        elif self.search_method == 'patient_address':
            self.screen_manager.add_widget(self.controller.find_by_address(input_data, page))
        elif self.search_method == 'doctor_name':
            self.screen_manager.add_widget(self.controller.find_by_doctor_name(input_data, page))
        elif self.search_method == 'appointment_date':
            self.screen_manager.add_widget(self.controller.find_by_appointment_date(input_data, page))

        self.screen_manager.add_widget(SearchScreen(name='search_screen'))
        self.screen_manager.add_widget(DeleteScreen(name='delete_screen'))
        
if __name__ == '__main__':
    Program().run()