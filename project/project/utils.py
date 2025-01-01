from typing import TypedDict
import argparse


class WindowSize(TypedDict):
    width: int
    height: int


def windowsize():
    parser = argparse.ArgumentParser(description="Configure game parameters.")
    parser.add_argument("--width", type=int, default=20, help="Width of the board.")
    parser.add_argument("--height", type=int, default=15, help="Height of the board.")
    parser.add_argument("--tile-size", type=int, default=20, help="Size of each tile.")
    parser.add_argument("--fps", type=int, default=10, help="Frames per second.")
    parser.add_argument("--fruit-color", type=str, default="#FF0000", help="Fruit color.")
    return vars(parser.parse_args())
