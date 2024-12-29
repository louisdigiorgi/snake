import argparse
import re

def parse_window_size():
    parser = argparse.ArgumentParser(description="Configure game parameters.")
    parser.add_argument("--width", type=int, default=20, help="Width of the game board.")
    parser.add_argument("--height", type=int, default=15, help="Height of the game board.")
    parser.add_argument("--tile-size", type=int, default=20, help="Size of each tile.")
    args = parser.parse_args()
    return args
