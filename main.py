from SetPixels import SetPixels
from GetFrames import GetFrames
from GetThresh import GetThresh
from MakeTrack import MakeTrack
from MakeVideo import MakeVideo
from CheckMask import CheckMask
from CreateCsv import CreateCsv
from Config import CONFIG, args1, args2, em1

import tkinter as tk
from tkinter import messagebox

params = CONFIG["params"]
diff1 = CONFIG["diff1"]
diff2 = CONFIG["diff2"]
track = CONFIG["track"]
contour = CONFIG["contour"]


class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("EasyTracker")
        self.img_dir = "/Users/miles/Documents/Python Projects/coding etc/Ed Hammill/Practice Miles sequence"  # DEV: change to ""
        self.params_f = self.img_dir + params  # DEV: change to ""
        self.diff_dirs = ["", ""]
        self.contour_json = ""
        self.track_json = ""

        # TODO: add help bar

        self.l0 = tk.Label(root, text="EasyTracker", font=('Helvetica', 30))
        self.l1 = tk.Label(root, text="Get help in the tab above", font=('Helvetica', 9, 'italic'))
        self.b0 = tk.Button(root, text="1) Make Frames/Start Where You Left Off ", command=self.getFrames, **args1)
        self.b1 = tk.Button(root, text="Optional -  Set Distance per Pixel      ", command=self.setPixels, **args2)
        self.b2 = tk.Button(root, text="2)       Set Threshold and Make Files   ", command=self.getThresh, **args1)
        self.b3 = tk.Button(root, text="3)      Make or Select track.json File  ", command=self.makeTrack, **args1)
        self.b4 = tk.Button(root, text="4)       Make Masked Video (Validate)   ", command=self.makeVideo, **args1)
        self.b5 = tk.Button(root, text="Optional -      Check Tracks            ", command=self.checkMask, **args2)
        self.b6 = tk.Button(root, text="5)           Generate .csv data         ", command=self.createCsv, **args1)
        self.b7 = tk.Button(root, text="                    Quit                ", command=self.quit, **args1)

        self.widgets = [self.l0, self.l1, self.b0, self.b1, self.b2,
                        self.b3, self.b4, self.b5, self.b6, self.b7]

        for widget in self.widgets:
            widget.pack(pady=5)

        tk.mainloop()

    def getFrames(self):
        temp = GetFrames(self.root)
        self.root.wait_window(temp.window)
        self.img_dir, self.params_f, self.diff_dirs, self.track_json, self.contour_json = temp.getFiles()
        if self.img_dir:
            self.b0.config(**args2)
        if self.contour_json:
            self.b2.config(**args2)
        if self.track_json:
            self.b3.config(**args2)

    def setPixels(self):
        if not self.img_dir:
            messagebox.showerror(title="Premature Selection", message=em1)
        else:
            temp = SetPixels(self.root, self.img_dir)
            self.root.wait_window(temp.window)
            self.params_f = temp.getInfo()
            if self.params_f:
                self.b1.config(**args2)

    def getThresh(self):
        if not self.img_dir:
            messagebox.showerror(title="Premature Selection", message=em1)
        else:
            temp = GetThresh(self.root, self.img_dir)
            self.root.wait_window(temp.window)
            self.diff_dirs = temp.getDirs()
            if self.diff_dirs[0]:
                self.b2.config(**args2)

    def makeTrack(self):
        if not self.diff_dirs[0]:
            pass
            # TODO: Warning message to point program towards frames & differences folders
        else:
            # TODO: ask if they want to use existing track files or make new ones
            makeNew = False
            temp = MakeTrack(self.root, self.img_dir, makeNew=makeNew)
            self.track_json = temp.getTrack()

    def makeVideo(self):
        if not self.track_json:
            pass
            # TODO: Warning message to point program towards frames, differences folders, track file
        else:
            # TODO: Ask which details they want (box, mask, etc, but num is required)
            MakeVideo(self.root, self.img_dir)
            # TODO: tell them where they can watch it

    def checkMask(self):
        if not self.track_json:
            pass
            # TODO: warning message to go thru the steps or find files
        else:
            CheckMask(self.root, self.img_dir)

    def createCsv(self):
        if not self.track_json:
            # TODO: warning message to generate such a thing
            pass
        else:
            # TODO: Tell them where it's saved
            CreateCsv(self.root, self.img_dir)

    def getScale(self):
        if not self.params_f:
            return 1, "pixels"
        else:
            pass
            # TODO: read in the deets from that .json

    def quit(self):
        self.root.destroy()


def main():
    try:
        root = tk.Tk()
        Main(root)
    except Exception as error:
        messagebox.showerror(title="Unknown Error", message="While running, this error occurred:\n" + str(error))


main()
