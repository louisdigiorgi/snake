import pygame
from .board import Board, CheckerBoard
from .snake import Snake
from .fruit import Fruit
from .direction import Dir
from .exceptions import GameOver
from .utils import windowsize

def game() -> None:
    DEFAULT_STARTING_SNAKE = [(10, 7), (10, 6), (10, 5)]
    DEFAULT_DIRECTION = Dir.RIGHT

    # Initialize the game window
    args = {
        "width": 20,
        "height": 15,
        "tile_size": 20,
        "fps": 10,
        "fruit_color": (255, 0, 0),
    }

    pygame.init()
    try:
        screen = pygame.display.set_mode(
            (args["width"] * args["tile_size"], args["height"] * args["tile_size"])
        )
        clock = pygame.time.Clock()
        pygame.display.set_caption("Snake - score : 0")

        board = Board(screen=screen, tile_size=args["tile_size"])
        checkerboard = CheckerBoard(
            {"width": args["width"], "height": args["height"]},
            (0, 0, 0), (255, 255, 255)
        )
        snake = Snake(DEFAULT_STARTING_SNAKE, (0, 255, 0), DEFAULT_DIRECTION)
        fruit = Fruit((3, 3), args["fruit_color"])
        board.add_object(checkerboard)
        board.add_object(snake)
        board.add_object(fruit)

        game_running = True
        while game_running:
            clock.tick(args["fps"])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake.dir != Dir.DOWN:
                        snake.dir = Dir.UP
                    elif event.key == pygame.K_DOWN and snake.dir != Dir.UP:
                        snake.dir = Dir.DOWN
                    elif event.key == pygame.K_RIGHT and snake.dir != Dir.LEFT:
                        snake.dir = Dir.RIGHT
                    elif event.key == pygame.K_LEFT and snake.dir != Dir.RIGHT:
                        snake.dir = Dir.LEFT

            try:
                snake.move(args["width"], args["height"])
                board.draw()
                pygame.display.set_caption(f"Snake - score : {len(snake) - 3}")
                pygame.display.update()
            except GameOver as e:
                print(e)  # Print "Game Over" message
                game_running = False
    finally:
        pygame.quit()
        print("Game Over!")
