import os
import io
import cv2
import json
import numpy as np
import tkinter as tk
from Progress import Progress
from Advanced import Advanced
import matplotlib.pyplot as plt
from PIL import Image, ImageTk, ImageOps
from Config import CONFIG, extension, params_dict

params = CONFIG["params"]
track = CONFIG["track"]
contour = CONFIG["contour"]
diff1 = CONFIG["diff1"]
diff2 = CONFIG["diff2"]
params_json = params_dict.copy()


def cvToPil(img):
    """Converts cv2 images to PIL images"""
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)


def makedir(dir_p):
    """Makes directory, or empties it if it is already there"""
    if os.path.isdir(dir_p):
        for f in os.listdir(dir_p):
            os.remove(dir_p + "/" + f)
    else:
        os.mkdir(dir_p)


class GetThresh:
    def __init__(self, root, folder):
        self.root = root
        self.folder = folder
        self.window = tk.Toplevel(self.root)
        self.done = False
        self.thresh = 10
        self.img = None
        self.picSize = (0, 0)
        self.hist = None
        self.histTk = None
        self.display = None
        self.displayTk = None
        self.canvas = None
        self.imgs = sorted(os.listdir(self.folder))
        for entry in range(len(self.imgs) - 1, -1, -1):
            temp = self.imgs[entry].rsplit(".")
            if len(temp) < 2 or temp[-1] not in extension:
                self.imgs.pop(entry)

        # Make folders necessary for tool
        self.diff1_p = self.folder + diff1
        self.diff2_p = self.folder + diff2
        self.contour = ""
        self.params = self.folder + params
        if os.path.exists(self.params):
            params_f = open(self.params)
            self.params_json = json.load(params_f)
            params_f.close()
        else:
            self.params_json = params_json
        makedir(self.diff1_p)
        makedir(self.diff2_p)

        # Advanced parameters
        self.canny_lower = self.params_json["canny_lower"]
        self.canny_upper = self.params_json["canny_upper"]
        self.kernel = self.params_json["kernel"]
        self.dilate_it = self.params_json["dilate_it"]
        self.erode_it = self.params_json["erode_it"]
        self.area_lower = self.params_json["area_lower"]
        self.area_upper = self.params_json["area_upper"]

        self.setup()

        # Make widgets to be placed in
        self.canvas = tk.Canvas(self.window, width=900, height=max(250, self.picSize[1]))
        self.canvas.create_image(self.picSize[0] / 2, self.picSize[1] / 2, anchor="center", image=self.displayTk)
        self.canvas.create_image(700, 100, anchor="center", image=self.histTk)
        self.slider = tk.Scale(self.window, from_=0, to=50, orient=tk.HORIZONTAL, length=297)
        self.slider.set(self.thresh)
        self.l0 = tk.Label(self.window, text="Histogram of Pixel Intensities")
        self.b0 = tk.Button(self.window, text="Show", command=self.getPic)
        self.b1 = tk.Button(self.window, text="Set & Run", command=self.setAndRun)
        self.b2 = tk.Button(self.window, text="Advanced", command=self.advanced)
        self.prog = Progress(self.window)

        self.getPic()
        self.slider.place(x=550, y=155)
        self.l0.place(x=615, y=20)
        self.b0.place(x=600, y=200)
        self.b1.place(x=655, y=200)
        self.b2.place(x=740, y=200)
        self.canvas.pack()

    def setup(self):
        """Gets the desired threshold for cut-off from user."""
        current2 = cv2.imread(self.folder + "/" + self.imgs[0])
        for indx in range(1, len(self.imgs)):  # Find a good difference example for user
            current1 = current2
            current2 = cv2.imread(self.folder + "/" + self.imgs[indx])
            diff = cv2.absdiff(current1, current2)
            if self.hasContent(diff):
                self.img = diff
                break

        vals = list(range(0, 50))
        freq = [i[0] for i in cv2.calcHist([self.img], [0], None, [256], [0, 256])][:50]

        plt.figure(figsize=(3, 1)).add_axes((0, 0, 1, 1))
        plt.bar(vals, freq, color='#0504aa')
        plt.axis("off")
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        self.hist = ImageOps.expand(Image.open(buf), 2, "black")
        self.histTk = ImageTk.PhotoImage(self.hist)
        self.size()

    def hasContent(self, image):
        """Returns true if an image has content above given threshold. False if otherwise."""
        _, baw = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), self.thresh, 255, cv2.THRESH_BINARY)
        return bool(np.amax(baw))

    def advanced(self):
        temp = Advanced(self.window, self.canny_lower, self.canny_upper, self.kernel, self.dilate_it, self.erode_it,
                        self.area_lower, self.area_upper)
        self.window.wait_window(temp.window)
        self.canny_lower, self.canny_upper, self.kernel, self.dilate_it, self.erode_it, \
            self.area_lower, self.area_upper = temp.getInfo()

    def size(self, scalar=500):
        w = int(self.img.shape[1])
        h = int(self.img.shape[0])
        scale_temp = scalar / w if w > h else scalar / h
        self.img = cv2.resize(self.img, (int(w * scale_temp), int(h * scale_temp)))
        self.picSize = (self.img.shape[1], self.img.shape[0])

    def getPic(self):
        """Make a new threshold picture based off of the current threshold and put it in the window"""
        self.thresh = int(self.slider.get())
        (_, baw) = cv2.threshold(cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY), self.thresh, 255, cv2.THRESH_BINARY)
        self.display = cvToPil(baw)
        self.displayTk = ImageTk.PhotoImage(self.display)
        self.canvas.create_image(self.picSize[0] / 2, self.picSize[1] / 2, anchor="center", image=self.displayTk)
        self.canvas.pack()

    def selectContours(self, contours):
        for indx in range(len(contours)-1, -1, -1):
            if cv2.contourArea(contours[indx]) < self.area_lower:
                contours.pop(indx)
            elif 0 < self.area_lower < self.area_upper < cv2.contourArea(contours[indx]):
                contours.pop(indx)

    def setAndRun(self):
        """Sets threshold based off of slider value and runs the difference"""
        if self.thresh != int(self.slider.get()):
            self.getPic()
        else:
            # window configuration
            self.b0.config(state=tk.DISABLED)
            self.b1.config(state=tk.DISABLED)
            self.b2.config(state=tk.DISABLED)
            self.prog.place(x=600, y=230)
            self.prog.config(length=len(self.imgs) * 2)

            # diff 1 files
            indx = 1
            name2 = self.imgs[0]
            current2 = cv2.imread(self.folder + "/" + name2)
            length = len(self.imgs)

            while indx < length:
                name1 = name2
                name2 = self.imgs[indx]
                current1 = current2
                current2 = cv2.imread(self.folder + "/" + name2)
                while not self.hasContent(cv2.absdiff(current1, current2)):  # skip frames w/o significant difference
                    indx += 1
                    self.prog.increase()
                    name2 = self.imgs[indx]
                    current2 = cv2.imread(self.folder + "/" + name2)
                temp = cv2.absdiff(current1, current2)  # difference between pictures
                temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)  # convert to grayscale
                temp = cv2.threshold(temp, self.thresh, 255, cv2.THRESH_TOZERO)[1]  # cut off all pixels below thresh
                temp = cv2.GaussianBlur(temp, (5, 5), 1)  # blur to get rid of remaining noise
                temp = cv2.Canny(temp, self.canny_lower, self.canny_upper)  # find edges with Canny algorithm
                cv2.imwrite(self.diff1_p + "/" + name1, temp)  # name is the name of the earlier image in the difference
                indx += 1
                self.prog.increase()

            # diff 2 files
            diff1_imgs = sorted(os.listdir(self.diff1_p))
            indx = 1
            self.contour = self.folder + contour
            contour_dict = {}
            kernel = np.ones((self.kernel, self.kernel))
            current2 = cv2.imread(self.diff1_p + "/" + diff1_imgs.pop(0))
            current2 = cv2.dilate(current2, kernel, iterations=self.dilate_it)
            current2 = cv2.erode(current2, kernel, iterations=self.erode_it)

            for image in diff1_imgs:
                current1 = current2
                current2 = cv2.imread(self.diff1_p + "/" + image)
                current2 = cv2.dilate(current2, kernel, iterations=self.dilate_it)
                current2 = cv2.erode(current2, kernel, iterations=self.erode_it)
                temp = cv2.bitwise_and(current1, current2)

                # collect and process contours
                contours = cv2.findContours(temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
                self.selectContours(contours)
                contour_dict[image] = contours

                # save image with contours
                temp = cv2.imread(self.folder + "/" + image)
                cv2.drawContours(temp, contours, -1, (0, 255, 0), 3)
                cv2.imwrite(self.diff2_p + "/" + image, temp)
                indx += 1
                self.prog.increase()

            f = open(self.contour, "w")
            json.dump(contour_dict, f)
            f.close()
            self.setParams()
            self.done = True
            self.window.destroy()

    def setParams(self):
        self.params_json["canny_lower"] = self.canny_lower
        self.params_json["canny_upper"] = self.canny_upper
        self.params_json["kernel"] = self.kernel
        self.params_json["dilate_it"] = self.dilate_it
        self.params_json["erode_it"] = self.erode_it
        self.params_json["area_lower"] = self.area_lower
        self.params_json["area_upper"] = self.area_upper
        f = open(self.params, "w")
        json.dump(f, self.params_json)
        f.close()

    def getDirs(self):
        """Return directories of difference pictures"""
        return [self.diff1_p, self.diff2_p] if self.done else ["", ""]
