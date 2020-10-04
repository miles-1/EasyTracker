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

    def reset(self):
        self.progress["value"] = 0
        self.root.update()

    def increase(self, num=1):
        temp = self.progress["value"]
        self.progress["value"] = min(temp + num * (100 - temp)/self.length, 100) if self.length else 100
        self.length = (self.length - num) if self.length - num > 0 else 0
        self.root.update()
