from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, ListProperty
from kivy.metrics import dp

class ButtonIcon(ButtonBehavior, Label):
    icon_source = StringProperty("default_icon.png")
    # Propriété pour la position de l'icône
    icon_pos = ListProperty([0, 0])