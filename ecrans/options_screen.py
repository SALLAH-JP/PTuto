from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
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

        config = load_config()
        
        for index in [ "nb_dechets", "largeur_plage", "longueur_plage", "taux_recyclage", "vitesse_simulation"]:

            value = self.parent.ids[index].text
            if value == "" : value = config[index]

            try:
                value = int( value )

                if value <= 0:
                    raise ValueError("Toutes les valeurs doivent être positives.")

            except ValueError as e:
                self.show_temporary_message(str(e))
                return

        for index in [ "nb_dechets", "largeur_plage", "longueur_plage", "taux_recyclage", "vitesse_simulation"]:

            value = self.parent.ids[index].text
            if value == "" : value = config[index]
            
            modify_variable(index, int(value))

        modify_variable("mode_avance", self.parent.ids.mode_avance.active)



    def show_temporary_message(self, message):
        """Affiche un message temporaire avec animation."""
        label = self.parent.ids.error_label
        label.text = message

        # Animation pour rendre le message visible et disparaître
        anim = Animation(opacity=1, duration=0.5) + Animation(opacity=0, duration=2)
        anim.start(label)



class OptionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options_widget = OptionsWidget()
        self.add_widget(self.options_widget)

    def on_pre_enter(self):
        self.options_widget.on_pre_enter()