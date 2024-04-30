import os
import pygame

# constants for colors
RED = [0xe3, 0x1b, 0x23]
BLUE = [0x00,0x2F,0x8B]
GREY = [0xA2, 0xAA, 0xAD]
WHITE = [0xFF, 0xFF, 0xFF]
BLACK = [0x00, 0x00, 0x00]
CYAN = [0x00, 0xBC, 0xBC]
MAGENTA = [0xBC, 0x00, 0xBC]
YELLOW = [0xBC, 0xBC, 0x00]
INK = [0x0A, 0x01, 0x1C]
PAPER = [0xEB, 0xED, 0xD1]
GRAPHITE = [0x6D, 0x75, 0x75]
BLOOD = [0x52, 0x0a, 0x02]


# keys from pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_y,
    K_n,
    KEYDOWN,
    QUIT,
    K_SPACE,
    MOUSEBUTTONUP,
    K_BACKSPACE,
    K_RETURN
)

#paths to sounds
STORM = os.path.join("room_explorer_audio", "rainstorm_cut.mp3")
BG_MUSIC = os.path.join("room_explorer_audio", "room_explorer_bg_music_compressed.wav")
RADIO = os.path.join("room_explorer_audio", "radio_with_static.wav")
SCARBOROUGH = os.path.join("room_explorer_audio", "scarborough.mp3")
WATERFALL = os.path.join("room_explorer_audio", "waterfall.mp3")
DESPERATE_RECORD = os.path.join("room_explorer_audio", "desperate_record_cut.mp3")
SCREAM = os.path.join("room_explorer_audio", "scream.mp3")
MUSIC_BOX = os.path.join("room_explorer_audio", "flight_of_the_confused_pigeon.mp3")
BONUS = os.path.join("room_explorer_audio", "bonus_record_full.mp3")
CREDITS = os.path.join("room_explorer_audio", "inverse_cut_room_explorer.wav")

#misc image paths
DEATH_SCREEN = os.path.join(os.path.join("room_explorer_graphics", "other"), "death.png")
DEATH_SCREEN = pygame.image.load(DEATH_SCREEN)

#constants for text
FONT_SIZE = 20
LINE_SPACING = 0

#list of symbols code is randomly generated from
OVEN_SYMBOLS = ["}", "#", "^", "&", "*", "|", ":", ".", "/", "?", "~", "`", ">", "=", "+", "-", "["]

