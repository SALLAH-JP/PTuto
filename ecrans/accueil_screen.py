from variables.config_manager import *
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class AccueilWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

    def on_simuler_pressed(self):
        """Vérifie si un robot est connecté et ouvre un Popup si aucun n'est trouvé."""
        conf = load_config()

        if not conf["robot_connect"]:
            self.afficher_popup()

    def afficher_popup(self):
        """Affiche un Popup pour avertir l'utilisateur et lui proposer de jouer."""

        box = BoxLayout(orientation="vertical", spacing=10, padding=10)
        label = Label(text="Aucun robot n'est connecté.\nVoulez-vous jouer en mode simulation ?")
        
        # Boutons pour le choix de l'utilisateur
        btn_oui = Button(text="Oui")
        btn_non = Button(text="Non", background_color=(1, 0, 0, 1))  # Rouge
        
        # Ajouter les boutons au layout vertical
        box.add_widget(label)
        box.add_widget(btn_oui)
        box.add_widget(btn_non)

        # Configuration du popup
        popup = Popup(title="Attention", content=box, size_hint=(0.6, 0.4), auto_dismiss=False)
        
        # Liens des boutons
        btn_oui.bind(on_press=lambda x: self.jouer_mode_simulation(popup))
        btn_non.bind(on_press=lambda x: popup.dismiss())
        
        # Affiche le popup
        popup.open()

    def jouer_mode_simulation(self, popup):
        """Action lorsque l'utilisateur choisit de jouer en mode simulation."""
        
        popup.dismiss()
        self.parent.manager.current = "simulation"


class AccueilScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.accueil_widget = AccueilWidget()
        self.add_widget(self.accueil_widget)

    def on_simuler_pressed(self):
        self.accueil_widget.on_simuler_pressed()