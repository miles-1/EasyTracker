import tkinter as tk
from Config import CONFIG

track = CONFIG["track"]
diff1 = CONFIG["diff1"]
diff2 = CONFIG["diff2"]


class MakeTrack:
    def __init__(self, img_folder, makeNew=True):
        self.trackjson = img_folder + track
        if makeNew:
            self.root_folder = img_folder
            self.diff_folders = [img_folder + diff1, img_folder + diff2]
            # TODO: make track.json files that keep track of where objects are frame
            #  by frame (along with their area & dimensions) and make good frame-by-frame guesses for who is who

    def getTrack(self):
        return self.trackjson
