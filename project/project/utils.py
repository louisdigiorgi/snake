from typing import TypedDict
import argparse


class WindowSize(TypedDict):
    width: int
    height: int


def windowsize() -> WindowSize:
    DEFAULT_WIDTH = 20
    DEFAULT_HEIGHT = 15
    DEFAULT_TILE_SIZE = 20
    DEFAULT_FPS = 10

    parser = argparse.ArgumentParser(description='Configure game parameters.')
    parser.add_argument('-w', '--width', type=int, default=DEFAULT_WIDTH,
                        help="Width of the game board in tiles (minimum: 20).")
    parser.add_argument('-e', '--height', type=int, default=DEFAULT_HEIGHT,
                        help="Height of the game board in tiles (minimum: 15).")
    parser.add_argument('--tile-size', type=int, default=DEFAULT_TILE_SIZE,
                        help="Size of each tile in pixels (minimum: 10, maximum: 100).")
    parser.add_argument('--fps', type=int, default=DEFAULT_FPS,
                        help="Frames per second (minimum: 3, maximum: 60).")
    parser.add_argument('--fruit-color', type=str, default='#FF0000',
                        help="Hexadecimal color code for the fruit (e.g., #FF0000).")
    parser.add_argument('--gameover-on-exit', action='store_true',
                        help="End the game if the snake exits the board.")
    args = parser.parse_args()

    # Validate arguments
    if args.width < 20:
        raise IntRangeError("width", args.width, 20, float('inf'))
    if args.height < 15:
        raise IntRangeError("height", args.height, 15, float('inf'))
    if not (10 <= args.tile_size <= 100):
        raise IntRangeError("tile-size", args.tile_size, 10, 100)
    if not (3 <= args.fps <= 60):
        raise IntRangeError("fps", args.fps, 3, 60)
    if not re.match(r'^#[0-9A-Fa-f]{6}$', args.fruit_color):
        raise ColorError(args.fruit_color, "fruit-color")

    return {
        "width": args.width,
        "height": args.height,
        "tile_size": args.tile_size,
        "fps": args.fps,
        "fruit_color": args.fruit_color,
        "gameover_on_exit": args.gameover_on_exit
    }

