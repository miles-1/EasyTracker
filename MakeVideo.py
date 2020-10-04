import tkinter as tk
from Config import CONFIG

track = CONFIG["track"]


class MakeVideo:
    def __init__(self, img_dir):
        self.img_dir = img_dir
        self.trackjson = img_dir + track
        self.options = 0
