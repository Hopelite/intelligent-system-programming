from kivy.app import App
from src.controllers.controllers import ViewAppointmentsController
from kivy.lang import Builder

Builder.load_file("src/views/views.kv")

class Program(App):

    def build(self):
        return ViewAppointmentsController().get_table()
        
if __name__ == '__main__':
    Program().run()