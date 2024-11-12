# Import des bibliothèques requises
import pygame
import argparse

# Définition de la taille des carrés du checkerboard
square_size = 20

# Classe pour dessiner des trucs
class Draw:
    def __init__(self, screen):
        self.screen = screen

    def draw_square(self, color, x, y):
        pygame.draw.rect(self.screen, color, (x, y, square_size, square_size))  # Dessine un carré de la couleur donnée à la position (x, y)


# Classe pour le damier
class Checkerboard:
    def __init__(self, width, height, drawer):
        self.width = width
        self.height = height
        self.drawer = drawer

    def draw(self):
        for y in range(0, self.height, square_size):
            for x in range(0, self.width, square_size):
                color = (255, 255, 255) if (x + y) // square_size % 2 == 0 else (0, 0, 0)  # Pour l'effet damier
                self.drawer.draw_square(color, x, y)


# Classe pour le serpent
class Snake:
    def __init__(self, initial_position, drawer):
        self.position = initial_position
        self.drawer = drawer

    def draw(self):
        for index, segment in enumerate(self.position):
            x, y = segment
            color = (0, 255 , 0) if index == 0 else (0, 70 , 0)  # Tête en vert clair, corps en vert foncé
            self.drawer.draw_square(color, x * square_size, y * square_size)


# Début du jeu
def snake():
    # Configuration des arguments pour la largeur et la hauteur
    parser = argparse.ArgumentParser(description="Configuration de la taille de la fenêtre du jeu")
    parser.add_argument('-W', '--width', type=int, default=800, help="Largeur de la fenêtre (par défaut: 800).")
    parser.add_argument('-H', '--height', type=int, default=600, help="Hauteur de la fenêtre (par défaut: 600).")
    args = parser.parse_args()

    # Pour que le damier soit plus joli, on arrondit la taille choisie pour avoir des carrés pleins et pas coupés aux bords
    width = (args.width // square_size) * square_size
    height = (args.height // square_size) * square_size

    # Initialisation de Pygame et création de la fenêtre
    pygame.init()
    screen = pygame.display.set_mode((width, height))

    # Création d'une instance de Draw pour dessiner les éléments
    drawer = Draw(screen)

    # Initialisation du damier et du serpent avec le dessinateur
    checkerboard = Checkerboard(width, height, drawer)
    snake = Snake([(5, 10), (6, 10), (7, 10)], drawer)  # Position initiale du serpent

    # Pour afficher l’écran
    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Pour pouvoir fermer le jeu avec la croix
                running = False

        # Dessin du damier et du serpent
        checkerboard.draw()
        snake.draw()

        # Mise à jour de l'affichage
        pygame.display.flip()

    # Quitter proprement Pygame
    pygame.quit()