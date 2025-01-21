import logging
import colorlog
from argparse import ArgumentParser
from .cmd_line import read_args
from .exceptions import SnakeError
from .game import Game

def setup_logger(verbose: bool) -> logging.Logger:
    """Set up the logger with color support and verbosity control."""
    log_level = logging.DEBUG if verbose else logging.INFO
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s[%(levelname)s] %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    ))

    logger = logging.getLogger("snake")
    logger.setLevel(log_level)
    logger.addHandler(handler)
    return logger


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    # Configure the logger
    logger = setup_logger(args.verbose)

    try:
        # Read command line arguments
        game_args = read_args()

        # Start the game
        logger.info("Starting the Snake game...")
        game = Game(
            width=game_args.width,
            height=game_args.height,
            tile_size=game_args.tile_size,
            fps=game_args.fps,
            fruit_color=game_args.fruit_color,
            snake_head_color=game_args.snake_head_color,
            snake_body_color=game_args.snake_body_color,
            gameover_on_exit=game_args.gameover_on_exit,
            scores=None,  # Replace if needed
            logger=logger,  # Pass the logger to the game
        )
        game.start()

    except SnakeError as e:
        logger.error(f"Error: {e}")
        exit(1)
