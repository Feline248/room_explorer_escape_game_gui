#Name: Rachel Dahl
#Item class with name and description
#I plan to add individual item images at a later point in time

from pygame import mixer
import os

class Item():

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @property                               #name
    def name(self):
        return self._name

    @name.setter
    def name(self, new_value):
        self._name = new_value

    @property                               #item description
    def item_descriptions(self):
        return self._item_descriptions

    @item_descriptions.setter
    def item_descriptions(self, new_value):
        self._item_descriptions = new_value

    def __str__(self):
        return self.description


class Grabbable(Item): #items that can be picked up and put in the inventory

    def __init__(self, name, description):
        Item.__init__(self, name, description)

        #some items set this to true when used, it prevents them from being used more than once
        self.single_use = False
        


class SoundItem(Item): #items that play sounds when looked at

    def __init__(self, name:str, description:str, sound_file:str): 
        '''
        descriptions of sound items should include a transcript of the sound played
        '''

        Item.__init__(self, name, description)
        self.sound_file = sound_file
        self.sound_path = os.path.join("room_explorer_audio", self.sound_file)

    @property                           #path to sound file to be played
    def sound_file(self):
        return self._sound_file

    @sound_file.setter
    def sound_file(self, new_value):
        self._sound_file = new_value
        self.sound_path = os.path.join("room_explorer_audio", self.sound_file)

    def play_sound(self): #prints the item's description and plays its associated sound
        mixer.music.load(self.sound_path)
        mixer.music.set_volume(0.7)
        mixer.music.play()
        for i in range(10):
            pass
        
        


class CodeItem(Item): #items that have a code that needs to be input

    def __init__(self, name:str, description:str, correct_code:str):
        Item.__init__(self, name, description)
        self.correct_code = correct_code

    @property                           #correct value that must be input to unlock the item
    def correct_code(self):
        return self._correct_code

    @correct_code.setter
    def correct_code(self, new_value):
        self._correct_code = new_value

    def __str__(self):
        response = self.description
        response += "\nYou can enter a code with the 'use' command."
        return response

