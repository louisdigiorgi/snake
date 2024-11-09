import pygame
import argparse
import sys

def snake():
    # Configurer les arguments pour la largeur et la hauteur avec argparse
    parser = argparse.ArgumentParser(description="Configurer la taille de la fenêtre du jeu Snake.")
    parser.add_argument('-W', '--width', type=int, default=800, help="Largeur de la fenêtre (par défaut: 800).")
    parser.add_argument('-H', '--height', type=int, default=600, help="Hauteur de la fenêtre (par défaut: 600).")
    args = parser.parse_args()

    # Initialiser Pygame et créer la fenêtre
    pygame.init()
    screen = pygame.display.set_mode((args.width, args.height))
    pygame.display.set_caption("Snake Game")

    # Couleur de fond
    background_color = (255, 255, 255)  # Blanc

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

        # Remplir l’écran avec la couleur de fond
        screen.fill(background_color)
        
        # Mettre à jour l'affichage
        pygame.display.flip()

    # Quitter proprement Pygame
    pygame.quit()
    sys.exit(0)  # Retourner le code de statut 0 pour indiquer une sortie correcte
