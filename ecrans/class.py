from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, NumericProperty
from kivy.metrics import dp

class ButtonIcon(ButtonBehavior, Label):
    icon_source = StringProperty("default_icon.png")
    icon_offset_x = NumericProperty(dp(40))

