import serial
#import bluetooth
import socket
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import serial.tools.list_ports
import threading
import queue


class RobotWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.baudrate = 115200
        self.arduino = None

    def select_port(self):
        ports = serial.tools.list_ports.comports()
        affiche = "PORT         DEVICE                     MANUFACTURER"
        for index, value in enumerate(sorted(ports)):
            if value.hwid != 'n/a':  # Vérifie que le port est valide
                affiche += f"\n{index}\t{value.name}\t{value.manufacturer}"

        self.parent.ids.dev.text = affiche
        
    def connect_usb(self):
        try:
            port = self.parent.ids.port_input.text
            self.arduino = serial.Serial(port, baudrate=self.baudrate, timeout=.1)
            self._update_status(f"Connexion au port {port} établie", True)
            modify_variable("mode_avance", robot_connect)
            modify_variable("port_usb", port)

        except Exception as e:
            self._update_status(f"Erreur lors de la configuration USB : {e}", False)


    def connect_wifi(self):
        try:
            # Création d'un socket TCP/IP
            ip = self.parent.ids.wifi_ip_input.text
            port = int (self.parent.ids.wifi_port_input.text)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)  # Définit un délai d'attente pour la connexion (en secondes)
            sock.connect((ip, port))  # Tente de se connecter à l'appareil via son IP et port

            # Envoie d'un message de test
            sock.sendall(b"PING\n")
            response = sock.recv(1024).decode().strip()

            if response == "PONG":
                self._update_status("Wi‑Fi connecté avec succès ✔️", True)
                modify_variable("robot_connect", True)
                modify_variable("ip", ip)
                modify_variable("port_wifi", port)
            else:
                self._update_status(f"Wi‑Fi: Réponse inattendue : {response}", False)

            return sock  # Retourne le socket, utile pour poursuivre la communication
        except Exception as e:
            self._update_status(f"Wi‑Fi Error: {e}", False)
            return None

    def _update_status(self, message, success=True):
        lbl = self.parent.ids.get('status_label')  # Widget pour afficher le statut
        if lbl:
            lbl.text = message
            lbl.color = (0, 1, 0, 1) if success else (1, 0, 0, 1)

class RobotScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.robot_widget = RobotWidget()
        self.add_widget(self.robot_widget)

    def connect_bluetooth(self, address):
        self.robot_widget.connect_bluetooth(address)

    def connect_wifi(self, ip, port):
        self.robot_widget.connect_wifi(ip, port)

    def on_enter(self):
        self.robot_widget.select_port()
