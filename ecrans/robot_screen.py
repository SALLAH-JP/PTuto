import serial
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

class RobotWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def connect_usb(self, port, baudrate=115200):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            self._update_status(f"USB: ouverture de {port}@{baudrate}", True)
            # Envoi d'un ping et lecture de la réponse
            Clock.schedule_once(lambda dt: self._test_usb(), 0.5)
        except serial.SerialException as e:
            self._update_status(f"USB Error: {e}", success=False)

    def _test_usb(self):
        try:
            self.ser.write(b'PING\n')
            resp = self.ser.readline().decode().strip()
            if resp == 'PONG':
                self._update_status("USB connecté ✔️", True)
            else:
                self._update_status(f"USB: réponse inattendue « {resp} »", False)
        except Exception as e:
            self._update_status(f"USB comm error: {e}", False)

    def connect_bluetooth(self, address):
        try:
            # Si aucune adresse fournie, on cherche un appareil nommé "robot"
            if not address:
                nearby = bluetooth.discover_devices(duration=8, lookup_names=True)
                for addr, name in nearby:
                    if 'robot' in name.lower():
                        address = addr
                        break
                if not address:
                    return self._update_status("Aucun robot BT trouvé", False)

            self.bt_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.bt_sock.connect((address, 1))
            self.bt_sock.send("PING\n".encode())
            resp = self.bt_sock.recv(1024).decode().strip()
            if resp == 'PONG':
                self._update_status("Bluetooth connecté ✔️", True)
            else:
                self._update_status(f"BT: réponse inattendue « {resp} »", False)
        except Exception as e:
            self._update_status(f"BT Error: {e}", False)

    def connect_wifi(self, ip, port=5000):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(3)
            self.sock.connect((ip, port))
            self.sock.sendall(b'PING\n')
            resp = self.sock.recv(1024).decode().strip()
            if resp == 'PONG':
                self._update_status("Wi‑Fi connecté ✔️", True)
            else:
                self._update_status(f"Wi‑Fi: réponse inattendue « {resp} »", False)
        except Exception as e:
            self._update_status(f"Wi‑Fi Error: {e}", False)

    def _update_status(self, message, success=True):
        lbl = self.parent.ids.get('status_label')
        if lbl:
            lbl.text = message
            lbl.color = (0,1,0,1) if success else (1,0,0,1)


class RobotScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.robot_widget = RobotWidget()
        self.add_widget(self.robot_widget)

    def connect_usb(self, port):
        self.robot_widget.connect_usb(port)

    def connect_bluetooth(self, address):
        self.robot_widget.connect_bluetooth(address)

    def connect_wifi(self, ip, port):
        self.robot_widget.connect_wifi(ip, port)
