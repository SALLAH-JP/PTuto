from variables.config_manager import *
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout

class AccueilWidget(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_simuler_pressed(self):
        """Vérifie si un robot est connecté et ouvre un MDDialog si aucun n'est trouvé."""
        conf = load_config()
        if not conf["robot_connect"]:
            self.afficher_popup()

    def afficher_popup(self):
        """Affiche un MDDialog pour avertir l'utilisateur et lui proposer de jouer en mode simulation."""
        self.dialog = MDDialog(
            title="Attention",
            text="Aucun robot n'est connecté.\nVoulez-vous jouer en mode simulation ?",
            buttons=[
                MDFlatButton(
                    text="Non", on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Oui", on_release=lambda x: self.jouer_mode_simulation(self.dialog)
                )
            ],
        )
        self.dialog.open()

    def jouer_mode_simulation(self, dialog):
        """Action lorsque l'utilisateur choisit de jouer en mode simulation."""
        dialog.dismiss()
        # On passe à l'écran "simulation" via le ScreenManager
        self.parent.manager.current = "simulation"


class AccueilScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.accueil_widget = AccueilWidget()
        self.add_widget(self.accueil_widget)

    def on_simuler_pressed(self):
        self.accueil_widget.on_simuler_pressed()