from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from ecrans.accueil_screen import AccueilScreen
from ecrans.simulation_screen import SimulationScreen
from ecrans.robot_screen import RobotScreen
from ecrans.options_screen import OptionsScreen
from kivy.core.window import Window
from kivy.lang import Builder

# Charger le fichier KV qui contient votre interface
Builder.load_file('interface.kv')

# Définir une taille minimale à la fenêtre
Window.minimum_width = 500
Window.minimum_height = 375

class MyScreenManager(ScreenManager):
    pass

class MainApp(MDApp):
    def build(self):
        # Configuration du thème KivyMD
        self.theme_cls.primary_palette = "Blue"   # Couleur primaire : Blue, par exemple
        self.theme_cls.theme_style = "Light"        # Options: "Light" ou "Dark"
        
        sm = MyScreenManager()
        # Votre fichier KV doit ajouter automatiquement les écrans à MyScreenManager
        sm.current = 'accueil'
        return sm

if __name__ == "__main__":
    MainApp().run()