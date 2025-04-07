import random
from variables.config_manager import *
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.clock import Clock



class SimulationWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SimulationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.simulation_widget = SimulationWidget()
        self.add_widget(self.simulation_widget)