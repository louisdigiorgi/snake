import pygame
import argparse
import sys

# Définir la taille des carrés du checkerboard
square_size = 20

# Définir la position initiale du serpent
snake_position = [(5, 10), (6, 10), (7, 10)]  # Coordonnées des segments du serpent (tête, corps, queue)

def draw_checkerboard(screen, width, height):
    """Dessine un damier noir et blanc sur l'écran."""
    for y in range(0, height, square_size):
        for x in range(0, width, square_size):
            # Alternance des couleurs pour créer l'effet de damier
            color = (255, 255, 255) if (x + y) // square_size % 2 == 0 else (0, 0, 0)
            pygame.draw.rect(screen, color, (x, y, square_size, square_size))

def draw_snake(screen):
    """Dessine le serpent sur l'écran."""
    for segment in snake_position:
        # Dessiner chaque segment du serpent en vert
        x, y = segment
        pygame.draw.rect(screen, (0, 255, 0), (x * square_size, y * square_size, square_size, square_size))

def snake():
    # Configurer les arguments pour la largeur et la hauteur avec argparse
    parser = argparse.ArgumentParser(description="Configurer la taille de la fenêtre du jeu Snake.")
    parser.add_argument('-W', '--width', type=int, default=800, help="Largeur de la fenêtre (par défaut: 800).")
    parser.add_argument('-H', '--height', type=int, default=600, help="Hauteur de la fenêtre (par défaut: 600).")
    args = parser.parse_args()

    # Arrondir la largeur et la hauteur pour qu'elles soient divisibles par la taille des carrés
    width = (args.width // square_size) * square_size
    height = (args.height // square_size) * square_size

    # Initialiser Pygame et créer la fenêtre
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")

    # Boucle principale pour afficher l’écran
    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre avec la croix
                running = False
            if event.type == pygame.KEYDOWN:  # Si une touche est pressée
                if event.key == pygame.K_q:  # Si la touche Q est pressée
                    running = False

        # Dessiner le damier sur l'écran
        draw_checkerboard(screen, width, height)
        
        # Dessiner le serpent sur l'écran
        draw_snake(screen)

        # Mettre à jour l'affichage
        pygame.display.flip()

    # Quitter proprement Pygame
    pygame.quit()
    sys.exit(0)  # Retourner le code de statut 0 pour indiquer une sortie correcte