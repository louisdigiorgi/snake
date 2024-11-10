# Import des bibliothèques requises
import pygame
import argparse
import sys

# Définition de la taille des carrés du checkerboard
square_size = 20

# Définition de la position initiale du serpent
snake_position = [(5, 10), (6, 10), (7, 10)]  # Respectivement (tête, corps, queue)

# Dessin du damier 
def checkerboard(screen, width, height):
    for y in range(0, height, square_size):
        for x in range(0, width, square_size):
            # Alternance des couleurs
            color = (255, 255, 255) if (x + y) // square_size % 2 == 0 else (0, 0, 0)
            pygame.draw.rect(screen, color, (x, y, square_size, square_size))

# Dessin du serpent
def snake_drawing(screen):
    for segment in snake_position:
        # Dessin de chaque segment du serpent en vert
        x , y = segment
        pygame.draw.rect(screen, (0, 255, 0), (x * square_size, y * square_size, square_size, square_size))

# Début du jeu
def snake():
    # Configuration des arguments pour la largeur et la hauteur 
    parser = argparse.ArgumentParser(description="Configuration de la taille de la fenêtre du jeu")
    parser.add_argument('-W', '--width', type=int, default=800, help="Largeur de la fenêtre (par défaut: 800).")
    parser.add_argument('-H', '--height', type=int, default=600, help="Hauteur de la fenêtre (par défaut: 600).")
    args = parser.parse_args()

    # Pour que le damier soit plus joli,
    # on arrondit la taille choisie pour avoir des carrés pleins et pas coupés aux bords
    width = (args.width // square_size) * square_size
    height = (args.height // square_size) * square_size

    # Initialisation de Pygame et création de la fenêtre
    pygame.init()
    screen = pygame.display.set_mode((width, height))

    # Pour afficher l’écran
    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Pour pouvoir fermer le jeu avec la croix
                running = False

        # Dessin du damier sur l'écran
        checkerboard(screen, width, height)
        
        # Dessin du serpent sur l'écran
        snake_drawing(screen)

        # Mise à jour de l'affichage
        pygame.display.flip()

    # Quitter proprement Pygame
    pygame.quit()
