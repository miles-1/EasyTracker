from PIL import Image, ImageDraw, ImageTk
import tkinter
import random


class SeeSeg:
    def __init__(self,name,img,root,annotations):
        
        self.annotations = annotations
        
        self.picSize = (0,0)
        self.originalSize = (0, 0)
        self.scale = 1.0

        self.size(img)  # sets pic sizes
        self.name = name
        self.root = root
        self.leave = False

        self.OGimg = img # keep copy of original image
        self.img = img.copy()
        self.draw = ImageDraw.Draw(self.img)
        self.Tkimg = ImageTk.PhotoImage(self.img)

        self.fills = ["red", "green", "white", "aqua", "beige", "blueviolet", "cyan", "cornsilk",
                      "darkgoldenrod", "darkorange", "mediumspringgreen", "darkolivegreen", "cadetblue",
                      "maroon", "skyblue", "greenyellow", "palevioletred", "crimson", "sandybrown"]
        self.fill = 0

        self.canvas = tkinter.Canvas(self.root, width = self.picSize[0], height = self.picSize[1]+50)
        self.realizePicSeg()
        instructions = tkinter.Label(self.root,text=self.name + "\nProgress: 'p'.  Change color: 'c'.  Quit: 'q'.")
        instructions.place(x=self.picSize[0]/5, y=self.picSize[1] + 10)

        self.root.bind("p", self.close)
        self.root.bind("c", self.changeColor)
        self.root.bind("q", self.quit)

        self.canvas.pack()

        tkinter.mainloop()

    def size(self, img, scale=1000):
        self.originalSize = img.size
        img.thumbnail((scale,scale))
        self.picSize = img.size
        self.scale = self.picSize[0]/self.originalSize[0]
    
    def realizePicSeg(self):
        self.img = self.OGimg.copy()
        tempImg = self.OGimg.copy()
        for name, segmentations in self.annotations.items():
            for seg in segmentations:
                if len(seg) > 2:
                    tempDraw = ImageDraw.Draw(tempImg)
                    self.draw = ImageDraw.Draw(self.img)

                    tempDraw.polygon([segi*self.scale for segi in seg],outline="black",fill=self.fills[self.fill])
                    self.draw.text([seg[0]*self.scale,(seg[1]-20)*self.scale],name,fill=self.fills[self.fill])
                    tempDraw.text([seg[0]*self.scale,(seg[1]-20)*self.scale],name,fill=self.fills[self.fill])

                    self.fill += 1
                    self.fill %= len(self.fills)

                    tempImg.putalpha(255)
                    self.img.putalpha(150)
                    tempImg = Image.alpha_composite(tempImg,self.img)
                    self.img = tempImg.copy()


        self.Tkimg = ImageTk.PhotoImage(tempImg)
        self.canvas.create_image(self.picSize[0]/2, self.picSize[1]/2, anchor="center", image=self.Tkimg)
        self.canvas.pack()
    
    def changeColor(self,event):
        self.fill = random.randint(0,len(self.fills)-1)
        self.realizePicSeg()

    def close(self,event):
        self.root.destroy()
    
    def quit(self,event):
        self.leave = True
        self.close(event)
    
    def isLeave(self):
        return self.leave