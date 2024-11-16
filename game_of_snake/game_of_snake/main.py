# Import des bibliothèques requises 
import pygame
import argparse
import random

# Définition des différentes tailles
SQUARE_SIZE = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Classe pour dessiner des trucs  
class Draw:
    def __init__(self, screen):
        self.screen = screen

    def draw_square(self, color, x, y):
        pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))  # Dessine un carré d'une certaine couleur en (x,y)

# Classe pour le damier
class Checkerboard:
    def __init__(self, width, height, drawer):
        self.width = width
        self.height = height
        self.drawer = drawer

    def draw(self):
        for y in range(0, self.height, SQUARE_SIZE):
            for x in range(0, self.width, SQUARE_SIZE):
                color = (255, 255, 255) if (x + y) // SQUARE_SIZE % 2 == 0 else (0, 0, 0)  # Pour l'effet damier
                self.drawer.draw_square(color, x, y)

# Classe pour le serpent 
class Snake:
    def __init__(self, initial_position, drawer):
        self.position = initial_position
        self.drawer = drawer
        self.direction = (1, 0)  # Le serpent commence par aller vers la droite
        self.grow_next = False  # Indique si le serpent doit grandir au prochain déplacement

    def move(self):  # Déplacements du serpent en fonction de la direction
        head_x, head_y = self.position[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Ajout de la nouvelle tête
        self.position = [new_head] + self.position

        # Si le serpent doit grandir, on ne supprime pas la queue
        if not self.grow_next:
            self.position.pop()
        else:
            self.grow_next = False  # Réinitialiser après avoir grandi

    def grow(self):  # Signaler que le serpent doit grandir
        self.grow_next = True

    def draw(self):
        for index, segment in enumerate(self.position):
            x, y = segment
            color = (0, 255, 0) if index == 0 else (0, 100, 0)  # Tête en vert clair, corps en vert foncé
            self.drawer.draw_square(color, x * SQUARE_SIZE, y * SQUARE_SIZE)

    def set_direction(self, new_direction):  # Pour empêcher le serpent de se retourner sur lui-même
        if (new_direction == (1, 0) and self.direction != (-1, 0)) or \
           (new_direction == (-1, 0) and self.direction != (1, 0)) or \
           (new_direction == (0, 1) and self.direction != (0, -1)) or \
           (new_direction == (0, -1) and self.direction != (0, 1)):
            self.direction = new_direction

# Classe pour le fruit
class Fruit:
    def __init__(self, drawer, width, height):
        self.drawer = drawer
        self.width = width
        self.height = height
        self.position = self.random_position()

    def random_position(self):  # Apparition aléatoire sur le damier
        return (random.randint(0, (self.width // SQUARE_SIZE) - 1), 
                random.randint(0, (self.height // SQUARE_SIZE) - 1))

    def draw(self):
        x, y = self.position
        self.drawer.draw_square((255, 0, 0), x * SQUARE_SIZE, y * SQUARE_SIZE)  # Fruit en rouge

# Début du jeu
def snake():
    # Configuration des arguments pour la largeur et la hauteur
    parser = argparse.ArgumentParser(description="Configuration de la taille de la fenêtre du jeu")
    parser.add_argument('-W', '--width', type=int, default=SCREEN_WIDTH, help="Largeur de la fenêtre (par défaut: 800).")
    parser.add_argument('-H', '--height', type=int, default=SCREEN_HEIGHT, help="Hauteur de la fenêtre (par défaut: 600).")
    args = parser.parse_args()

    # Pour que le damier soit plus joli, on arrondit la taille choisie pour avoir des carrés pleins et pas coupés aux bords
    width = (args.width // SQUARE_SIZE) * SQUARE_SIZE
    height = (args.height // SQUARE_SIZE) * SQUARE_SIZE

    # Initialisation de Pygame et création de la fenêtre
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Jeu du Serpent")

    # Création d'une instance de Draw pour dessiner les éléments
    drawer = Draw(screen)

    # Initialisation du damier, du serpent et du fruit avec le dessinateur
    checkerboard = Checkerboard(width, height, drawer)
    snake = Snake([(5, 10), (4, 10), (3, 10)], drawer)  # Position initiale du serpent
    fruit = Fruit(drawer, width, height)  # Fruit initialisé à une position aléatoire

    # Variables de jeu
    fruit_count = 0
    clock = pygame.time.Clock()

    # Boucle principale
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.set_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.set_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.set_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction((1, 0))

        # Déplacement du serpent
        snake.move()

        # Vérification de la collision avec un fruit
        if snake.position[0] == fruit.position:
            snake.grow()
            fruit = Fruit(drawer, width, height)
            fruit_count += 1

        # Vérification des collisions avec les bords ou soi-même
        head_x, head_y = snake.position[0]
        if head_x < 0 or head_x >= width // SQUARE_SIZE or head_y < 0 or head_y >= height // SQUARE_SIZE or \
           len(snake.position) != len(set(snake.position)):
            print("Game Over! Score:", fruit_count)
            running = False

        # Dessin de l'écran
        checkerboard.draw()
        snake.draw()
        fruit.draw()

        # Pour afficher le score
        font = pygame.font.SysFont("Arial", 28)
        score_text = font.render(f"Fruits mangés: {fruit_count}", True, (0, 0, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()