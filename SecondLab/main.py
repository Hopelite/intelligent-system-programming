from kivy.app import App
from views import TableScreen
from kivy.lang import Builder

Builder.load_file("views.kv")

class Program(App):

    def build(self):
        return TableScreen()
        
if __name__ == '__main__':
    Program().run()