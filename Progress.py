from tkinter.ttk import Progressbar
from tkinter import HORIZONTAL


class Progress:
    def __init__(self, root, length=1):
        self.root = root
        self.length = length
        self.progress = Progressbar(self.root, orient=HORIZONTAL, length=200, mode='determinate')

    def pack(self, **kwargs):
        self.progress.pack(**kwargs)

    def place(self, **kwargs):
        self.progress.place(**kwargs)

    def config(self, length):
        self.length = int(length)

    def increase(self):
        temp = self.progress["value"]
        self.progress["value"] = min(temp + (100 - temp)/self.length, 100)
        self.length -= 1 if self.length > 0 else 0
        self.root.update()
