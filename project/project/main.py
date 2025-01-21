# ruff: noqa: D100,S311

 

# Standard

import sys

 

# First party

from .cmd_line import read_args

from .exceptions import SnakeError

from .game import Game

from .score import Score

from .scores import Scores  # Assure-toi que cette importation est correcte

 

def main() -> None:  # noqa: D103

    try:

        # Read command line arguments

        args = read_args()

 

        # Load scores from the YAML file

        scores = Scores.load("high_scores.yaml")  # Charge les scores du fichier YAML

 

        # Start game and pass the current scores to it

        game = Game(width=args.width, height=args.height,

                    tile_size=args.tile_size, fps=args.fps,

                    fruit_color=args.fruit_color,

                    snake_head_color=args.snake_head_color,

                    snake_body_color=args.snake_body_color,

                    gameover_on_exit=args.gameover_on_exit,

                    scores=scores)  # Passe les scores à la logique du jeu

 

        # Start the game

        game.start()

 

        # After the game, handle the player's score

        if game.is_game_over():  # Assure-toi d’avoir une méthode `is_game_over` dans Game

            # Ask for player's name and add score to the scores list

            player_name = input("Enter your name: ")

            player_score = game.get_player_score()  # Récupère le score du joueur

            player_score_obj = Score(score=player_score, name=player_name)

            scores.add_score(player_score_obj)

 

            # Save updated scores to the file

            scores.save("high_scores.yaml")

 

    except SnakeError as e:

        print(f"Error: {e}")  # noqa: T201

        sys.exit(1)