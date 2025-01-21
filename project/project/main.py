# ruff: noqa: D100,S311

# Standard
import sys

# First party
from .cmd_line import read_args
from .exceptions import SnakeError
from .game import Game
from .score import Score
from .scores import Scores  # Assure-toi que cette importation est correcte

def main() -> None:
    try:
        # Lire les arguments de la ligne de commande
        args = read_args()

        # Charger les scores depuis le fichier YAML
        scores = Scores.load("high_scores.yaml")

        # Démarrer le jeu
        game = Game(
            width=args.width,
            height=args.height,
            tile_size=args.tile_size,
            fps=args.fps,
            fruit_color=args.fruit_color,
            snake_head_color=args.snake_head_color,
            snake_body_color=args.snake_body_color,
            gameover_on_exit=args.gameover_on_exit,
            scores=scores,
        )
        game.start()

    except SnakeError as e:
        print(f"Error: {e}")
        sys.exit(1)

