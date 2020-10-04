import tkinter as tk
from Config import CONFIG

track = CONFIG["track"]


class CheckMask:
    def __init__(self, img_folder):
        # TODO: have the JSON instructions mask the objects according to checkboxes. On the right, show a scrollbar
        #  list of which nums are in the screen and which aren't. Allow for users to go between frames with keyboard.
        #  Users can click on one individual and can delete, move or exchange it with another from there on out.
        #  Addition is not possible in GUI but can be added to track_json manually via a separate thing (?)
        self.img_folder = img_folder
        self.track_json = img_folder + track
