import random
import math
import time
from variables.config_manager import *
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.clock import Clock



class SimulationWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nb_dechets = 10
        self.score_dechet = 0
        self.dechets = []
        self.dechets_ratio = []
        self.robot_ratio = ( 0, 0 )
        self.dechet_size = (100, 100)
        self.en_cours = False
        self.etat_simulation = False

        # Met à jour la position du robot si la fenêtre est redimensionnée
        self.bind(height=self.update_robot_position, width=self.update_robot_position)
        self.bind(height=self.update_dechets_position, width=self.update_dechets_position)

    def generate_robot(self):

        if not hasattr(self, 'robot'): #self.parent.ids.simulatio_widget.canvas.remove(self.robot)

            with self.parent.ids.simulation_widget.canvas:

                Color(1, 1, 1, 1)
                self.robot = Rectangle(
                    source="assets/robot/robot.jpg",
                    pos=(15, 15),
                    size=(50, 50)
                )

            self.robot_ratio = ( 15/self.parent.ids.simulation_widget.width, 15/self.parent.ids.simulation_widget.height )

    def generate_dechets(self):

        if not self.en_cours:
            self.clear_dechets()

            config = load_config()
            nb_dechets = config["nb_dechets"]

            for _ in range(nb_dechets):
                # Position aléatoire dans la zone graphique
                random_x = random.randint(0, int(self.parent.ids.simulation_widget.width))
                random_y = random.randint(0, int(self.parent.ids.simulation_widget.height))

                with self.parent.ids.simulation_widget.canvas:
                    dechet = Rectangle(
                        source="assets/dechets/dechet.png",
                        pos=(random_x, random_y),
                        size=self.dechet_size,
                    )

                self.dechets.append(dechet)
                self.dechets_ratio.append((random_x/self.parent.ids.simulation_widget.width, random_y/self.parent.ids.simulation_widget.height))

    def clear_dechets(self):
        """Efface les anciens déchets du canvas."""
        for dechet in self.dechets:
            self.parent.ids.simulation_widget.canvas.remove(dechet)
        self.dechets = []
        self.dechets_ratio = []

    def update_robot_position(self, *args):
        """Met à jour la position du robot en fonction de la nouvelle taille du widget."""
        pos_x = int( self.robot_ratio[0] * self.parent.ids.simulation_widget.width )
        pos_y = int( self.robot_ratio[1] * self.parent.ids.simulation_widget.height )

        self.robot.pos = ( pos_x, pos_y )

    def update_dechets_position(self, *args):
        """Met à jour la position des déchets en fonction de la nouvelle taille du widget."""
        index = 0
        for dechet in self.dechets:

            pos_x = int( self.dechets_ratio[index][0] * self.parent.ids.simulation_widget.width )
            pos_y = int( self.dechets_ratio[index][1] * self.parent.ids.simulation_widget.height )

            dechet.pos = (pos_x, pos_y)
            index += 1


    def update(self, dt):

        #direction
        x, y = self.robot.pos

        # Calculer la nouvelle position horizontale
        x = x + self.step * self.direction

        # Si le robot atteint un bord, verrouille la position et change de ligne
        if x < 15 or x > self.parent.ids.simulation_widget.width - 5:
            # Contraindre à l'intérieur
            x = max(15, min(x, self.parent.ids.simulation_widget.width - 5))
            # Monter d'une ligne
            y += self.row_step
            y = max(15, min(y, self.parent.ids.simulation_widget.height - 5))
            # Inverser la direction
            self.direction *= -1

        self.robot.pos = (x, y)
        self.robot_ratio = (x / self.parent.ids.simulation_widget.width, y / self.parent.ids.simulation_widget.height)
        robot_width, robot_height = self.robot.size

        # Vérifier la collision avec chacun des déchets
        for dechet in self.dechets[:]:
            dechet_x, dechet_y = dechet.pos
            dechet_width, dechet_height = dechet.size
            
            # Vérifie si le robot est au-dessus du déchet
            if (x < dechet_x + dechet_width and
                x + robot_width > dechet_x and
                y < dechet_y + dechet_height and
                y + robot_height > dechet_y):

                self.parent.ids.simulation_widget.canvas.remove(dechet)
                self.dechets.remove(dechet)
                self.score_dechet += 1

        # Si le robot atteint le haut de la zone de jeu, arrêter le parcours
        if y == self.parent.ids.simulation_widget.height - 5:
            self.stop_simulation()


    def parcours_classique(self):

        # S'assurer que le robot existe
        if not hasattr(self, 'robot'):
            self.generate_robot()
        
        # Placer le robot en bas à gauche
        self.robot.pos = (15, 15)
        self.robot_ratio = ( 15/self.parent.ids.simulation_widget.width, 15/self.parent.ids.simulation_widget.height )
        
        # Paramètres du parcours
        self.step = 10          # Pas horizontal en pixels
        self.row_step = 50      # Pas vertical à chaque changement de ligne
        self.direction = 1      # 1: mouvement vers la droite, -1: vers la gauche

        config = load_config()
        vitesse = config["vitesse_simulation"]
        Clock.schedule_interval(self.update, 0.1 / vitesse)


    def parcours_spirale(self):
        pass


    def parcours_random(self):
        pass



    def demarrer_simulation(self):
            
        self.etat_simulation = not self.etat_simulation
        self.parent.ids.bouton.icon_source = "assets/icones/icone_pause.png" if self.etat_simulation else "assets/icones/icone_start.png"

        if not self.en_cours:
            choix = self.parent.ids.parcours_spinner.text
            if choix == "Parcours Classique":
                self.en_cours = True
                self.parcours_classique()
            elif choix == "Parcours Spirale":
                self.en_cours = True
                self.parcours_spirale()
            elif choix == "Parcours Aléatoire":
                self.en_cours = True
                self.parcours_random()
            elif choix == "Parcours 4":
                pass
        else:
            if not self.etat_simulation:
                Clock.unschedule(self.update)
            else:
                config = load_config()
                vitesse = config["vitesse_simulation"]
                Clock.schedule_interval(self.update, 0.1 / vitesse)


    def stop_simulation(self):
        Clock.unschedule(self.update)
        self.etat_simulation = False
        self.en_cours = False
        self.parent.ids.bouton.icon_source = "assets/icones/icone_start.png"

        self.robot.pos = (15, 15)
        self.robot_ratio = ( 15/self.parent.ids.simulation_widget.width, 15/self.parent.ids.simulation_widget.height )



class SimulationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.simulation_widget = SimulationWidget()
        self.add_widget(self.simulation_widget)
        self.first_time = True

    def on_pre_enter(self):
        self.simulation_widget.generate_robot()

    def on_enter(self):
        if self.first_time:
            self.first_time = False
            self.simulation_widget.generate_dechets()
