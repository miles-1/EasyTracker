import json
import tkinter as tk
import cv2
from tkinter import filedialog, messagebox
from Progress import Progress
import os
from Config import CONFIG, params_dict

params = CONFIG["params"]
diff1 = CONFIG["diff1"]
diff2 = CONFIG["diff2"]
track = CONFIG["track"]
contour = CONFIG["contour"]
params_json = params_dict.copy()


def makedir(dir_p):
    """Makes directory, or empties it if it is already there"""
    if os.path.isdir(dir_p):
        for f in os.listdir(dir_p):
            os.remove(dir_p + "/" + f)
    else:
        os.mkdir(dir_p)


class GetFrames:
    def __init__(self, root):
        self.root = root
        self.img_dir = ""
        self.perSec = -1
        self.params_json = ""
        self.diff_dirs = ["", ""]
        self.track_json = ""
        self.contour_json = ""

        self.window = tk.Toplevel(self.root)
        self.window.geometry("350x200")
        self.l0 = tk.Label(self.window, text="Select the video to process into frames,\n"
                                             "entering the number of frames per second to extract\n"
                                             "(default 0 means extract all frames available)\n"
                                             "-or- select the directory containing frames:")
        self.e0 = tk.Entry(self.window, width=4)
        self.e0.insert(0, "0")
        self.b0 = tk.Button(self.window, text="Select video", command=self.getFrames)
        self.l1 = tk.Label(self.window, text="-or-")
        self.b1 = tk.Button(self.window, text="Select folder", command=self.getFolder)
        self.prog = Progress(self.window)

        self.l0.pack()
        self.e0.pack()
        self.b0.pack()
        self.l1.pack()
        self.b1.pack()

    def getFrames(self):
        f = filedialog.askopenfilename()
        if isinstance(f, str) and self.e0.get().isdigit():
            self.img_dir = f
            video = cv2.VideoCapture(f)
            progress, frame = video.read()
            (i, frameCount) = (0, 0)
            fps = video.get(cv2.CAP_PROP_FPS)
            self.perSec = min(int(self.e0.get()), fps)
            ratio = int(fps // int(self.perSec)) if self.perSec else 1
            length_of_vid = int(video.get(cv2.CAP_PROP_FRAME_COUNT) // ratio)

            self.l0.config(text=f"~{length_of_vid} frames to convert for video. Video fps: {fps}. "
                                f"\nRatio of frames extracted per total: {ratio}.")
            self.e0.pack_forget()
            self.b0.pack_forget()
            self.l1.pack_forget()
            self.b1.pack_forget()
            self.prog.pack()
            self.window.update()

            self.img_dir = f[:f.rfind(".")] + " sequence"
            makedir(self.img_dir)

            if len(str(length_of_vid)) < len(str(length_of_vid + 5)):
                length_of_vid = length_of_vid + 5

            form = "0>" + str(len(str(length_of_vid)))
            self.prog.config(length=length_of_vid/10)

            while progress:
                if i % ratio == 0:
                    cv2.imwrite(f"{self.img_dir}/image{format(frameCount, form)}.jpg", cv2.UMat(frame))
                    frameCount += 1
                i += 1
                progress, frame = video.read()
                if i % (ratio * 10) == 0:
                    self.prog.increase()

            video.release()
            self.params_json = self.img_dir + params_json
            if os.path.exists(self.params_json):
                f = open(self.params_json)
                temp = json.load(f)
                f.close()
            else:
                temp = params_json
            temp["duration"] = ratio / fps
            f = open(self.params_json, "w")
            json.dump(temp, f)
            f.close()
            self.exit()
        else:
            messagebox.showerror(title="Bad ratio", message="Please type a non-negative integer "
                                                            "for the frame ratio entry box.")

    def getFolder(self):
        self.img_dir = filedialog.askdirectory()
        if self.img_dir:
            self.params_json = self.img_dir + params
            self.diff_dirs = [self.img_dir + diff1, self.img_dir + diff2]
            self.track_json = self.img_dir + track
            self.contour_json = self.img_dir + contour
            if not os.path.exists(self.params_json):
                self.params_json = ""
            if not (os.path.exists(self.diff_dirs[0]) and os.path.exists(self.diff_dirs[1]) and
                    len(os.listdir(self.diff_dirs[0])) and len(os.listdir(self.diff_dirs[1]))):
                self.diff_dirs = ["", ""]
            if not os.path.exists(self.contour_json):
                self.contour_json = ""
            if not os.path.exists(self.track_json):
                self.track_json = ""
            self.exit()

    def exit(self):
        self.window.destroy()

    def getFiles(self):
        return self.img_dir, self.params_json, self.diff_dirs, self.track_json, self.contour_json
