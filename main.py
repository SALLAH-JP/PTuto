from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from ecrans.accueil_screen import AccueilScreen
from ecrans.simulation_screen import SimulationScreen
from ecrans.robot_screen import RobotScreen
from ecrans.options_screen import OptionsScreen
from kivy.core.window import Window
from kivy.lang import Builder

Builder.load_file('interface.kv')

# Définir les tailles minimales ici
Window.minimum_width = 500
Window.minimum_height = 375


class MyScreenManager(ScreenManager):
    pass

class MainApp(App):
    def build(self):

        sm = MyScreenManager()
        sm.current = 'accueil'
        return sm

if __name__ == "__main__":
    MainApp().run()