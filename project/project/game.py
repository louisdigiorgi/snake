import os
import pygame
import typing
from .board import Board
from .checkerboard import Checkerboard
from .dir import Dir
from .exceptions import GameOver
from .fruit import Fruit
from .game_object import GameObject
from .score import Score
from .scores import Scores  
from .snake import Snake
from .state import State

# Constants
SK_START_LENGTH = 3
MAX_LENGTH = 8
MAX_SCORES = 5


class Game:
    """The main class of the game."""

    def __init__(self, width: int, height: int, tile_size: int,  # noqa: PLR0913
                 fps: int, *,
                 fruit_color: pygame.Color,
                 snake_head_color: pygame.Color,
                 snake_body_color: pygame.Color,
                 gameover_on_exit: bool,
                 scores, logger) -> None:
        """Object initialization."""
        self._width = width
        self._height = height
        self._tile_size = tile_size
        self._fps = fps
        self._fruit_color = fruit_color
        self._snake_head_color = snake_head_color
        self._snake_body_color = snake_body_color
        self._gameover_on_exit = gameover_on_exit
        self._snake = None
        self._new_high_score = None | Score
        self._scores = Scores.load("high_scores.yaml")  # Loading scores
        self._player_name = ""  # Store the player's name
        self._logger = logger
        self._logger.info("Game initialized.")


    def _reset_snake(self) -> None:
        """Reset the snake."""
        if self._snake is not None:
            self._board.detach_obs(self._snake)
            self._board.remove_object(self._snake)
            self._logger.debug("Resetting the snake.")
        self._snake = Snake.create_random(
            nb_lines=self._height, nb_cols=self._width,
            length=SK_START_LENGTH, head_color=self._snake_head_color,
            body_color=self._snake_body_color, gameover_on_exit=self._gameover_on_exit,
        )
        self._board.add_object(self._snake)
        self._board.attach_obs(self._snake)
        self._logger.debug("Snake has been created.")

    def _init(self) -> None:
        """Initialize the game."""
        screen_size = (self._width * self._tile_size, self._height * self._tile_size)
        self._screen = pygame.display.set_mode(screen_size)
        self._clock = pygame.time.Clock()
        self._board = Board(screen=self._screen, nb_lines=self._height, nb_cols=self._width, tile_size=self._tile_size)
        self._checkerboard = Checkerboard(nb_lines=self._height, nb_cols=self._width)
        self._board.add_object(self._checkerboard)
        self._reset_snake()
        Fruit.color = self._fruit_color
        self._board.create_fruit()

        # Load fonts 
        font_path = os.path.join(os.path.dirname(__file__), "DejaVuSansMono-Bold.ttf")
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")
        self._font_1 = pygame.font.Font(font_path, 32)
        self._font_2 = pygame.font.Font(font_path, 64)

    def _drawgameover(self) -> None:
        """Draw the gameover's sentence."""
        text_gameover = self._font_2.render("GAME OVER", True, pygame.Color("red"))
        x, y = 80, 160  # Define the position where to write text.
        self._screen.blit(text_gameover, (x, y))

    def _draw_scores(self) -> None:
        """Display the list of high scores."""
        x, y = 80, 10  # Define the position where to write text.
        for score in self._scores:
            text_scores = self._font_1.render(score.name.ljust(Score.MAX_LENGTH) + f" {score.score: >8}", True, pygame.Color("red"))
            self._screen.blit(text_scores, (x, y))
            y += 32
        pygame.display.update()

    def _draw_inputname(self) -> None:
        """Draw the input name screen."""
        text = self._font_1.render(f"Enter your name: {self._new_high_score.name}", True, pygame.Color("red"))
        x, y = 80, 10
        self._screen.blit(text, (x, y))
        pygame.display.update()

    def _process_scores_event(self, event: pygame.event.Event) -> None:
        """Switch to the state Play if needed."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._state = State.PLAY

    def _process_play_event(self, event: pygame.event.Event) -> None:
        """Change the direction of the snake if needed."""
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_UP:
                    self._snake.dir = Dir.UP
                case pygame.K_DOWN:
                    self._snake.dir = Dir.DOWN
                case pygame.K_LEFT:
                    self._snake.dir = Dir.LEFT
                case pygame.K_RIGHT:
                    self._snake.dir = Dir.RIGHT

    def _process_inputname(self, event: pygame.event.Event) -> None:
        """The player enters his/her name in the ranking list of highscores."""
        if self._new_high_score is not None and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  
                self._player_name = self._new_high_score.name  
                self._scores.add_score(self._new_high_score)  # Add or refresh the score
                self._scores.save("high_scores.yaml")  
                self._state = State.SCORES 
            elif event.key == pygame.K_BACKSPACE:  
                self._new_high_score.name = self._new_high_score.name[:-1]
            else:
                self._new_high_score.name += event.unicode

    def _process_events(self) -> None:
        """Process pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._state = State.QUIT
                self._logger.info("Quit event detected.")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Press 'Q' to quit
                    self._state = State.QUIT
                    self._logger.warning("Player pressed 'Q' to quit.")
                match self._state:
                    case State.SCORES:
                        self._process_scores_event(event)
                    case State.PLAY:
                        self._process_play_event(event)
                    case State.INPUT_NAME:
                        self._process_inputname(event)

    def is_game_over(self) -> bool:
        """Check if the game is in the GAMEOVER state."""
        return self._state == State.GAMEOVER

    def start(self) -> None:
        """Start the game."""
        pygame.init()
        self._logger.info("Pygame initialized.")
        self._init()
        self._state = State.SCORES
        self._logger.debug("Game state set to SCORES.")

        while self._state != State.QUIT:
            self._clock.tick(self._fps)
            self._process_events()
            try:
                if self._state == State.PLAY:
                    self._snake.move()
                    self._logger.debug("Snake moved.")

            except GameOver:
                self._state = State.GAMEOVER
                self._logger.info("Game over state reached.")
                countdown = self._fps
            self._screen.fill(pygame.Color("black"))
            self._board.draw()
            match self._state:
                case State.GAMEOVER:
                    self._drawgameover()
                    countdown -= 1
                    if countdown == 0:
                        score = self._snake.score
                        self._reset_snake()
                        if self._scores.is_highscore(score):
                            default_name = self._player_name if self._player_name else ""
                            self._new_high_score = Score(name=default_name, score=score)
                            if not self._player_name:
                                self._state = State.INPUT_NAME
                            else:
                                self._scores.add_score(self._new_high_score)
                                self._state = State.SCORES
                        else:
                            self._state = State.SCORES
                case State.SCORES:
                    self._draw_scores()
                case State.INPUT_NAME:
                    self._draw_inputname()
            pygame.display.update()
        self._logger.info("Game ended. Exiting...")
        pygame.quit()
