from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

class RobotWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def connect_robot(self, robot_ip, robot_port):
        """Méthode pour simuler la connexion au robot."""
        self.parent.ids.status_label.text = f"Connexion en cours à {robot_ip}:{robot_port}..."
        self.parent.ids.status_label.color = (1, 0.65, 0, 1)  # Orange pour indiquer l'action en cours

        # Simulation d'une tentative de connexion après 2 secondes
        Clock.schedule_once(lambda dt: self._simulate_connection(robot_ip, robot_port), 2)

    def _simulate_connection(self, ip, port):

        if port.upper() == "COM3":
            self.parent.ids.status_label.text = "Connexion établie avec succès."
            self.parent.ids.status_label.color = (0, 1, 0, 1)  # Vert pour succès
        else:
            self.parent.ids.status_label.text = "Échec de la connexion."
            self.parent.ids.status_label.color = (1, 0, 0, 1)  # Rouge pour échec


class RobotScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.robot_widget = RobotWidget()
        self.add_widget(self.robot_widget)

    def connect_robot(self, robot_ip, robot_port):
        self.robot_widget.connect_robot(robot_ip, robot_port)