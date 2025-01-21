import importlib.resources

import pygame

import typing

 

from .board import Board

from .checkerboard import Checkerboard

from .dir import Dir

from .exceptions import GameOver

from .fruit import Fruit

from .game_object import GameObject

from .score import Score

from .scores import Scores  # Importation des scores

from .snake import Snake

from .state import State

 

# Constants

SK_START_LENGTH = 3

MAX_LENGHT = 8

MAX_SCORES = 5

 

class Game:

    """The main class of the game."""

 

    def __init__(self, width: int, height: int, tile_size: int,  # noqa: PLR0913

                 fps: int,

                 *,

                 fruit_color: pygame.Color,

                 snake_head_color: pygame.Color,

                 snake_body_color: pygame.Color,

                 gameover_on_exit: bool,

                 scores

                 ) -> None:

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

 

        # Chargement des scores depuis le fichier YAML

        self._scores = Scores.load("high_scores.yaml")

 

    def _reset_snake(self) -> None:

        """Reset the snake."""

        if self._snake is not None:

            self._board.detach_obs(self._snake)

            self._board.remove_object(self._snake)

        self._snake = Snake.create_random(

                nb_lines=self._height,

                nb_cols=self._width,

                length=SK_START_LENGTH,

                head_color=self._snake_head_color,

                body_color=self._snake_body_color,

                gameover_on_exit=self._gameover_on_exit,

        )

        self._board.add_object(self._snake)

        self._board.attach_obs(self._snake)

 

    def _init(self) -> None:

        """Initialize the game."""

        # Create a display screen

        screen_size = (self._width * self._tile_size,

                       self._height * self._tile_size)

        self._screen = pygame.display.set_mode(screen_size)

 

        # Create the clock

        self._clock = pygame.time.Clock()

 

        # Create the main board

        self._board = Board(screen=self._screen,

                            nb_lines=self._height,

                            nb_cols=self._width,

                            tile_size=self._tile_size)

 

        # Create checkerboard

        self._checkerboard = Checkerboard(nb_lines=self._height,

                                          nb_cols=self._width)

        self._board.add_object(self._checkerboard)

 

        # Create snake

        self._reset_snake()

 

        # Create fruit

        Fruit.color = self._fruit_color

        self._board.create_fruit()

 

        # Download font

        with importlib.resources.path("snake", "DejaVuSansMono-Bold.ttf") as f:

            self._font_1 = pygame.font.Font(f, 32)

            self._font_2 = pygame.font.Font(f, 64)

 

    def _drawgameover(self) -> None:

        """Draw the gameover's sentence."""

        text_gameover = self._font_2.render("GAME OVER", True, pygame.Color("red"))

        x, y = 80, 160  # Define the position where to write text.

        self._screen.blit(text_gameover, (x, y))

 

    def _draw_scores(self) -> None:

        """Put a highscore's line."""

        x, y = 80, 10  # Define the position where to write text.

        for score in self._scores:

            text_scores = self._font_1.render(score.name.ljust(Score.MAX_LENGTH) + f" {score.score: >8}", True, pygame.Color("red"))

            self._screen.blit(text_scores, (x, y))

            y += 32

        pygame.display.update()

 

    def _draw_inputname(self) -> None:

        """Draw the input name screen."""

        text = self._font_1.render(f"Enter your name: {self._new_high_score.name}", True, pygame.Color("red"))

        x, y = 80, 10  # Position of the text

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

            if event.key == pygame.K_RETURN:  # Validate the name

                # Save the score with the player's name

                self._scores.add_score(self._new_high_score)  # Add the score with the name

                self._scores.save("high_scores.yaml")  # Save the scores in the YAML file

                self._state = State.SCORES  # Return to the scores screen, not quit

            elif event.key == pygame.K_BACKSPACE:  # Correct a mistake

                self._new_high_score.name = self._new_high_score.name[:-1]

            else:

                # Add a character to the name

                self._new_high_score.name += event.unicode

 

    def _process_events(self) -> None:

        """Process pygame events."""

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self._state = State.QUIT  # Properly handle quit event

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:  # Press 'Q' to quit

                    self._state = State.QUIT

                # Handle other states

                match self._state:

                    case State.SCORES:

                        self._process_scores_event(event)

                    case State.PLAY:

                        self._process_play_event(event)

                    case State.INPUT_NAME:

                        self._process_inputname(event)

 

    def start(self) -> None:

        """Start the game."""

        # Initialize pygame

        pygame.init()

 

        # Initialize game

        self._init()

 

        # Start pygame loop

        self._state = State.SCORES

        while self._state != State.QUIT:

 

            # Wait 1/FPS second

            self._clock.tick(self._fps)

 

            # Listen for events

            self._process_events()

 

            # Update objects

            try:

                if self._state == State.PLAY:

                    self._snake.move()

 

            except GameOver:

                self._state = State.GAMEOVER

                countdown = self._fps

 

            # Clear the screen before drawing the next frame

            self._screen.fill(pygame.Color("black"))

 

            # Draw

            self._board.draw()

            match self._state:

                case State.GAMEOVER:

                    self._drawgameover()

                    countdown -= 1

                    if countdown == 0:

                        score = self._snake.score

                        self._reset_snake()

                        if self._scores.is_highscore(score):

                            self._new_high_score = Score(name="", score=score)

                            self._state = State.INPUT_NAME  # Switch to name input state

                        else:

                            self._state = State.SCORES

                case State.SCORES:

                    self._draw_scores()

                case State.INPUT_NAME:

                    self._draw_inputname()

 

            # Display

            pygame.display.update()

 

        # Terminate pygame

        pygame.quit()