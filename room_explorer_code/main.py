                                                                                                                                         
# Name: Rachel Dahl
                                                                                                                                         
# Description: 
# A text-based puzzle game. The goal is to 
# solve all of the puzzles and escape the house.
                                                                                                                                         
# Improvements: 
#Item is now a seperate class
#There are 3 child classes of Item: Grabbable, SoundItem, and CodeItem
#controls and inventory can now be printed
#puzzles and an end goal of escaping were added
#some scenes and items play sounds
#added bonus puzzles that aren't part of the main story
#added the keyword 'use' to use objects and enter codes
#added some fun secret commands that the player can figure out
#added a hints system
                                                                                                                                         
#######MAIN#######
                                                                                                                                         
from game import Game

g = Game()

g.play()




