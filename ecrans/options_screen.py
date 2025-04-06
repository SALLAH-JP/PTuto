from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from variables.config_manager import *

class OptionsWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self):
        # Avant d'afficher l'écran, charger la configuration et remplir les champs
        config = load_config()

        self.parent.ids.nb_dechets.text = ""
        self.parent.ids.largeur_plage.text = ""
        self.parent.ids.longueur_plage.text = ""
        self.parent.ids.taux_recyclage.text = ""
        self.parent.ids.vitesse_simulation.text = ""

        self.parent.ids.nb_dechets.hint_text = str( config.get("nb_dechets", "") )
        self.parent.ids.largeur_plage.hint_text = str( config.get("largeur_plage", "") )
        self.parent.ids.longueur_plage.hint_text = str( config.get("longueur_plage", "") )
        self.parent.ids.taux_recyclage.hint_text = str( config.get("taux_recyclage", "") )
        self.parent.ids.vitesse_simulation.hint_text = str( config.get("vitesse_simulation", "") )
        self.parent.ids.mode_avance.active = config.get("mode_avance", False)


    def enregistrer_parametres(self):

        modify_variable("nb_dechets", self.parent.ids.nb_dechets.text)
        modify_variable("largeur_plage", self.parent.ids.largeur_plage.text)
        modify_variable("longueur_plage", self.parent.ids.longueur_plage.text)
        modify_variable("taux_recyclage", self.parent.ids.taux_recyclage.text)
        modify_variable("vitesse_simulation", self.parent.ids.vitesse_simulation.text)
        modify_variable("mode_avance", self.parent.ids.mode_avance.active)


class OptionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options_widget = OptionsWidget()
        self.add_widget(self.options_widget)

    def enregistrer_parametres(self):
        self.options_widget.enregistrer_parametres()

    def on_pre_enter(self):
        self.options_widget.on_pre_enter()