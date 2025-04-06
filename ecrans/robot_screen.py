from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock

class RobotWidget(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
    
    def connect_robot(self, robot_ip, robot_port):
        """Méthode pour simuler la connexion au robot."""
        # Mise à jour du status via l'id `status_label`
        self.parent.ids.status_label.text = f"Connexion en cours à {robot_ip}:{robot_port}..."
        # Pour MDLabel, on utilisera la propriété `text_color`
        self.parent.ids.status_label.text_color = (1, 0.65, 0, 1)  # Orange
        
        # Simulation d'une tentative de connexion après 2 secondes
        Clock.schedule_once(lambda dt: self._simulate_connection(robot_ip, robot_port), 2)
    
    def _simulate_connection(self, ip, port):
        # Simuler le résultat de la connexion
        if port.upper() == "COM3":
            self.parent.ids.status_label.text = "Connexion établie avec succès."
            self.parent.ids.status_label.text_color = (0, 1, 0, 1)  # Vert
        else:
            self.parent.ids.status_label.text = "Échec de la connexion."
            self.parent.ids.status_label.text_color = (1, 0, 0, 1)  # Rouge

class RobotScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.robot_widget = RobotWidget()
        self.add_widget(self.robot_widget)
    
    def connect_robot(self, robot_ip, robot_port):
        self.robot_widget.connect_robot(robot_ip, robot_port)