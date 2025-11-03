from art import text2art
import random
import os

FONTS = ["big", "colossal", "slant", "3-d"]

def ascii_art(word):
    """ ASCII art for our cinema application with random fonts """
    font = random.choice(FONTS)
    return text2art(word, font=font, chr_ignore=True)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")