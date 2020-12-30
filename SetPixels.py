import os
import json
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from Config import CONFIG, params_dict
from PIL import Image, ImageDraw, ImageTk, UnidentifiedImageError

params = CONFIG["params"]
params_json = params_dict.copy()
colors = ["red", "green", "white", "black"]


class SetPixels:
    def __init__(self, root, img_dir):
        self.root = root
        self.params_f = img_dir + params
        if os.path.exists(self.params_f):
            f = open(self.params_f)
            self.params_json = json.load(f)
            f.close()
        else:
            self.params_json = params_json
        self.scale = self.params_json["scale"]
        self.units = self.params_json["units"]

        # Data fields for Image Measurement
        self.line = []
        self.picSize = (0, 0)
        self.originalSize = (0, 0)
        self.scale = 1.0
        self.original_img = None
        self.img = None
        self.draw = None
        self.Tkimg = None
        self.color = 0
        self.frame = None

        self.window = tk.Toplevel(self.root)
        self.l0 = tk.Label(self.window, text="Enter the scale and units per pixel\n"
                                             "below and click 'Submit Scale'.\n"
                                             "-or- Calculate the scale from \n"
                                             "an image with 'Find from Image'.\n"
                                             "-or- Use pixel units by\n"
                                             "clicking 'Pixel Units'.")
        self.e0 = tk.Entry(self.window, width=10)
        self.e0.insert(0, self.params_json["scale"])
        self.e1 = tk.Entry(self.window, width=4)
        self.e1.insert(0, self.params_json["units"])
        self.b0 = tk.Button(self.window, text="Submit Scale", command=self.submit)
        self.l1 = tk.Label(self.window, text="-or-")
        self.b1 = tk.Button(self.window, text="Find from Image", command=self.getScale)
        self.l2 = tk.Label(self.window, text="-or-")
        self.b2 = tk.Button(self.window, text="Pixel Units", command=self.default)

        self.l0.grid(row=1, column=1, columnspan=3)
        self.e0.grid(row=2, column=1)
        self.e1.grid(row=2, column=2)
        self.b0.grid(row=2, column=3)
        self.l1.grid(row=3, column=1, columnspan=3)
        self.b1.grid(row=4, column=1, columnspan=3)
        self.l2.grid(row=5, column=1, columnspan=3)
        self.b2.grid(row=6, column=1, columnspan=3)

    def submit(self):
        if self.e0.get().replace(".", "").isdigit():
            if len(self.line) == 4:
                self.scale = float(self.e0.get()) / ((self.line[0] - self.line[2]) ** 2 +
                                                     (self.line[1] - self.line[3]) ** 2) ** 0.5
            else:
                self.scale = float(self.e0.get())
            self.units = self.e1.get()
            self.exit()
        else:
            messagebox.showerror(title="Non-number entered", message="The scale field was supposed to be a "
                                                                     "positive number but isn't.")

    def default(self):
        self.scale = 1.0
        self.units = "pixels"
        self.exit()

    def exit(self):
        self.write()
        self.window.destroy()

    def write(self):
        self.params_json["scale"] = self.scale
        self.params_json["units"] = self.units
        try:
            f = open(self.params_f, "w")
            json.dump(self.params_json, f)
            f.close()
        except PermissionError as error:
            messagebox.showerror(title="Permission denied", message="The frames folder you selected has incorrect "
                                                                    "permissions: " + str(error))

    def getScale(self):
        f = filedialog.askopenfilename(title="Select scale image")
        if isinstance(f, str) and f:
            self.l0.grid_forget()
            self.e0.grid_forget()
            self.e1.grid_forget()
            self.b0.grid_forget()
            self.l1.grid_forget()
            self.b1.grid_forget()
            self.l2.grid_forget()
            self.b2.grid_forget()

            try:
                self.original_img = Image.open(f)
                self.size()  # sets pic sizes
                self.img = self.original_img.copy()
                self.draw = ImageDraw.Draw(self.img)
                self.Tkimg = ImageTk.PhotoImage(self.img)
                self.frame = tk.Frame(self.window)
                self.l0 = tk.Label(self.window, image=self.Tkimg)
                instructions = tk.Label(self.window, text="Click on the image to set length.")
                self.e0 = tk.Entry(self.frame, width=4)
                self.e0.insert(0, "1")
                desc1 = tk.Label(self.frame, text="[length]")
                self.e1 = tk.Entry(self.frame, width=4)
                self.e1.insert(0, "pixel")
                desc2 = tk.Label(self.frame, text="[units]")
                self.b0 = tk.Button(self.frame, text="Submit Scale", command=self.submit)
                self.e0.grid(row=1, column=1)
                desc1.grid(row=1, column=2)
                self.e1.grid(row=1, column=3)
                desc2.grid(row=1, column=4)
                self.b0.grid(row=1, column=5)

                break1 = tk.Label(self.window, text="|")
                self.b1 = tk.Button(self.window, text="Undo", command=self.decreaseSeg)
                break2 = tk.Label(self.window, text="|")
                self.b2 = tk.Button(self.window, text="Change Color", command=self.changeColor)
                self.l0.grid(row=1, column=1, columnspan=5)
                instructions.grid(row=2, column=1, columnspan=5)
                self.frame.grid(row=3, column=1)
                break1.grid(row=3, column=2)
                self.b1.grid(row=3, column=3)
                break2.grid(row=3, column=4)
                self.b2.grid(row=3, column=5)

                self.activity()
            except UnidentifiedImageError as error:
                messagebox.showerror(title="Bad image file", message=str(error))
                self.getScale()

    def size(self, scalar=800):
        self.originalSize = self.original_img.size
        self.original_img.thumbnail((scalar, scalar*3/5))
        self.picSize = self.original_img.size
        self.scale = self.originalSize[0]/self.picSize[0]

    def activity(self):
        self.l0.bind('<Motion>', lambda event: self.onPic() if event.y <= self.picSize[1] else self.offPic())

    def onPic(self):
        self.l0.config(cursor='pencil')
        self.l0.bind('<Button-1>', self.increaseSeg)

    def offPic(self):
        self.l0.config(cursor='')
        self.l0.bind('<Button-1>', lambda x: None)

    def increaseSeg(self, event):
        if len(self.line) <= 2:
            self.line.extend([event.x, event.y])
            self.realizePicSeg()

    def decreaseSeg(self):
        if len(self.line) >= 2:
            self.line = self.line[:-2]
            self.realizePicSeg()

    def realizePicSeg(self):
        self.img = self.original_img.copy()
        if len(self.line) == 2:
            self.draw = ImageDraw.Draw(self.img)
            temp = [self.line[0] - 2, self.line[1] - 2] + [self.line[0] + 2, self.line[1] + 2]
            self.draw.ellipse(temp, fill=colors[self.color])
        elif len(self.line) == 4:
            self.draw = ImageDraw.Draw(self.img)
            self.draw.line(self.line, fill=colors[self.color], width=2)

        self.Tkimg = ImageTk.PhotoImage(self.img)
        self.l0.config(image=self.Tkimg)

    def changeColor(self):
        self.color += 1
        self.color %= len(colors)
        self.realizePicSeg()

    def getInfo(self):
        return self.params_f
