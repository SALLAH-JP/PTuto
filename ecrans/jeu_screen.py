import random
from variables.config_manager import *
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.clock import Clock



class JeuWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dechets = []
        self.dechets_ratio = []
        self.robot_ratio = (0, 0.5)
        self.dechet_size = (100, 100)

        # Met à jour la position du robot si la fenêtre est redimensionnée
        self.bind(height=self.update_robot_position, width=self.update_robot_position)
        self.bind(height=self.update_dechets_position, width=self.update_dechets_position)

    def generate_robot(self):

        if not hasattr(self, 'robot'): #self.parent.ids.jeu_widget.canvas.remove(self.robot)

            with self.parent.ids.jeu_widget.canvas:

                Color(1, 1, 1, 1)
                self.robot = Rectangle(
                    source="assets/robot/robot.jpg",
                    pos=(0, self.center_y - 25),
                    size=(50, 50)
                )

    def generate_dechets(self):

        self.clear_dechets()

        config = load_config()
        nb_dechets = int( config["nb_dechets"] )

        for _ in range(nb_dechets):
            # Position aléatoire dans la zone graphique
            random_x = random.randint(0, int(self.width - self.dechet_size[0]))
            random_y = random.randint(0, int(self.height - self.dechet_size[1]))

            with self.parent.ids.jeu_widget.canvas:
                dechet = Rectangle(
                    source="assets/dechets/dechet.png",
                    pos=(random_x, random_y),
                    size=self.dechet_size,
                )

            self.dechets.append(dechet)
            self.dechets_ratio.append((random_x/self.width, random_y/self.height))


    def clear_dechets(self):
        """Efface les anciens déchets du canvas."""
        for dechet in self.dechets:
            self.parent.ids.jeu_widget.canvas.remove(dechet)
        self.dechets = []
        self.dechets_ratio = []

    def update_robot_position(self, *args):
        """Met à jour la position du robot en fonction de la nouvelle taille du widget."""
        pos_x = int( self.robot_ratio[0] * self.width )
        pos_y = int( self.robot_ratio[1] * self.height )

        self.robot.pos = ( pos_x, pos_y )

    def update_dechets_position(self, *args):
        """Met à jour la position des déchets en fonction de la nouvelle taille du widget."""
        index = 0
        for dechet in self.dechets:

            pos_x = int( self.dechets_ratio[index][0] * self.width )
            pos_y = int( self.dechets_ratio[index][1] * self.height )

            dechet.pos = (pos_x, pos_y)
            index += 1

    def on_key_down(self, window, key, scancode, text, modifiers):
        """Déplace le robot en fonction de la touche pressée."""
        step = 10
        current_x, current_y = self.robot.pos

        if key == 276:  # Flèche gauche
            current_x -= step
        elif key == 275:  # Flèche droite
            current_x += step
        elif key == 273:  # Flèche haut
            current_y += step
        elif key == 274:  # Flèche bas
            current_y -= step

        # Assure que le robot reste dans les limites de l'écran
        current_x = max(0, min(self.width - self.robot.size[0], current_x))
        current_y = max(0, min(self.height - self.robot.size[1], current_y))

        self.robot.pos = (current_x, current_y)
        self.robot_ratio = ( current_x/self.width, current_y/self.height )



class JeuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.jeu_widget = JeuWidget()
        self.add_widget(self.jeu_widget)

    def generate_dechets(self):
        self.jeu_widget.generate_dechets()

    def on_pre_enter(self):
        self.jeu_widget.generate_robot()

    def on_enter(self):
        self.jeu_widget.generate_dechets()
        Window.bind(on_key_down=self.jeu_widget.on_key_down)

    def on_leave(self):
        Window.unbind(on_key_down=self.jeu_widget.on_key_down)

