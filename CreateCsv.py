import tkinter as tk
from Config import CONFIG

csv = CONFIG["csv"]
track = CONFIG["track"]


class CreateCsv:
    def __init__(self, root, img_dir):
        self.root = root
        self.track_json = img_dir + track
        # TODO: convert track.json to .csv file that shows individual's position/size across time and each of their
        #  average speed/size as well as the total average speed and size
