from kivy.app import App
from src.controllers.controllers import ViewAppointmentsController
from kivy.lang import Builder

Builder.load_file("src/views/views.kv")

class Program(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ViewAppointmentsController().start_program()

    def build(self):
        return self.screen_manager
        
if __name__ == '__main__':
    Program().run()