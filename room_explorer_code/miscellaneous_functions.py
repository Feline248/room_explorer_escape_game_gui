from constants import *
from pygame import mixer
import textwrap

def restart_bg_music():
        """adjusts volume and restarts normal background 
        music after another sound is played"""
        mixer.music.set_volume(0.4)
        mixer.music.load(BG_MUSIC)
        mixer.music.play()




