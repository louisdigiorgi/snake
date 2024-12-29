from .board import Board, CheckerBoard
from .snake import Snake
from .fruit import Fruit
from .tile import Tile
from .direction import Dir
from .exceptions import GameOver
from .utils import WindowSize
import pygame

def game() -> None:
    args = WindowSize()  # Parse command-line arguments

    print(f"Args in game(): {args}")  # Debugging line
    pygame.init()

    try:
        screen = pygame.display.set_mode(
            (args["width"] * args["tile_size"], args["height"] * args["tile_size"])
        )
        clock = pygame.time.Clock()
        pygame.display.set_caption("Snake - score : 0")
        board = Board(screen, args["tile_size"])
        snake = Snake([(10, 7), (10, 6), (10, 5)], (0, 255, 0), Dir.RIGHT)
        fruit = Fruit((3, 3), args["fruit_color"])
        board.add_object(snake)
        board.add_object(fruit)

        # Main game loop
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
                pygame.display.update()
            except GameOver as e:
                print(e)
                game_running = False
    finally:
        pygame.quit()
        print("Game Over!")

if __name__ == "__main__":
    game()