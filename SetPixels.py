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
            f = open(self.params_json)
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
        self.canvas = None

        self.window = tk.Toplevel(self.root)
        self.l0 = tk.Label(self.window, text="Enter the scale and units per pixel below and hit 'Submit Scale'.\n"
                                             "-or- Calculate the scale from an image with 'Find from Image.'\n"
                                             "-or- Use pixel units by hitting 'Pixel Units'.")
        self.e0 = tk.Entry(self.window, width=4)
        self.e0.insert(0, self.params_json["scale"])
        self.e1 = tk.Entry(self.window, width=4)
        self.e1.insert(0, self.params_json["units"])
        self.b0 = tk.Button(self.window, text="Submit Scale", command=self.submit)
        self.l1 = tk.Label(self.window, text="-or-")
        self.b1 = tk.Button(self.window, text="Find from Image", command=self.getScale)
        self.l2 = tk.Label(self.window, text="-or-")
        self.b2 = tk.Button(self.window, text="Pixel Units", command=self.default)

        self.l0.pack()
        self.e0.pack()
        self.e1.pack()
        self.b0.pack()
        self.l1.pack()
        self.b1.pack()
        self.l2.pack()
        self.b2.pack()

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
        self.scale = self.params_json["scale"]
        self.units = self.params_json["units"]
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
            self.window.resizable(False, False)
            self.l0.pack_forget()
            self.e0.pack_forget()
            self.e1.pack_forget()
            self.b0.pack_forget()
            self.l1.pack_forget()
            self.b1.pack_forget()
            self.l2.pack_forget()
            self.b2.pack_forget()

            try:
                self.original_img = Image.open(f)
                self.size()  # sets pic sizes
                self.img = self.original_img.copy()
                self.draw = ImageDraw.Draw(self.img)
                self.Tkimg = ImageTk.PhotoImage(self.img)

                self.canvas = tk.Canvas(self.window, width=self.picSize[0], height=self.picSize[1] + 150)
                self.canvas.create_image(self.picSize[0] / 2, self.picSize[1] / 2, anchor="center", image=self.Tkimg)
                instructions = tk.Label(self.window, text="Click on the image to set length.\n"
                                                          "Entry boxes: [length of line] [unit of length]")
                self.e0 = tk.Entry(self.window, width=4)
                self.e0.insert(0, "1")
                self.e1 = tk.Entry(self.window, width=4)
                self.e1.insert(0, "pixel")
                self.b0 = tk.Button(self.window, text="Submit Scale", command=self.submit)
                self.b1 = tk.Button(self.window, text="Undo", command=self.decreaseSeg)
                self.b2 = tk.Button(self.window, text="Change Color", command=self.changeColor)
                instructions.place(x=10, y=self.picSize[1] + 10)
                self.e0.place(x=10, y=self.picSize[1] + 60)
                self.e1.place(x=60, y=self.picSize[1] + 60)
                self.b0.place(x=110, y=self.picSize[1] + 60)
                self.b1.place(x=10, y=self.picSize[1] + 90)
                self.b2.place(x=10, y=self.picSize[1] + 120)

                self.canvas.pack()
                self.activity()
            except UnidentifiedImageError as error:
                messagebox.showerror(title="Bad image file", message=str(error))
                self.getScale()

    def size(self, scalar=1000):
        self.originalSize = self.original_img.size
        self.original_img.thumbnail((scalar, scalar))
        self.picSize = self.original_img.size
        self.scale = self.originalSize[0]/self.picSize[0]

    def activity(self):
        self.canvas.bind('<Motion>', lambda event: self.onPic() if event.y <= self.picSize[1] else self.offPic())

    def onPic(self):
        self.canvas.config(cursor='pencil')
        self.canvas.bind('<Button-1>', self.increaseSeg)

    def offPic(self):
        self.canvas.config(cursor='')
        self.canvas.bind('<Button-1>', lambda x: None)

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
        self.canvas.create_image(self.picSize[0] / 2, self.picSize[1] / 2, anchor="center", image=self.Tkimg)
        self.canvas.pack()

    def changeColor(self):
        self.color += 1
        self.color %= len(colors)
        self.realizePicSeg()

    def getInfo(self):
        return self.params_f
