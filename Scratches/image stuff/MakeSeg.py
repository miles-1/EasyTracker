from PIL import Image, ImageDraw, ImageTk
import tkinter


class MakeSeg:
    def __init__(self, name, img, root):
        self.segmentation = []
        self.annotations = []
        
        self.picSize = (0,0)
        self.originalSize = (0, 0)
        self.scale = 1.0

        self.size(img)  # sets pic sizes
        self.name = name
        self.root = root

        self.OGimg = img # keep copy of original image
        self.img = img.copy()
        self.draw = ImageDraw.Draw(self.img)
        self.Tkimg = ImageTk.PhotoImage(self.img)

        self.colors = ["red", "green", "white", "aqua", "beige", "blueviolet", "cyan", "cornsilk",
                      "darkgoldenrod", "darkorange", "mediumspringgreen", "darkolivegreen", "cadetblue",
                      "maroon", "skyblue", "greenyellow", "palevioletred", "crimson", "sandybrown"]
        self.color = 0

        self.canvas = tkinter.Canvas(self.root, width = self.picSize[0], height = self.picSize[1]+50)
        self.canvas.create_image(self.picSize[0]/2, self.picSize[1]/2, anchor="center", image=self.Tkimg)
        instructions = tkinter.Label(self.root,text="Undo: Backspace.  Change color: 'c'.\nProgress: 'p'.  Restart: 'r'.  New: 'n'.")
        instructions.place(x=10, y=self.picSize[1] + 10)

        self.root.bind("<BackSpace>", self.decreaseSeg)
        self.root.bind("c", self.changeColor)
        self.root.bind("p", self.harvest)
        self.root.bind("r", self.restart)
        self.root.bind("n", self.new)

        self.canvas.pack()

        self.activity()
        tkinter.mainloop()

    def size(self, img, scale=1000):
        self.originalSize = img.size
        img.thumbnail((scale, scale))
        self.picSize = img.size
        self.scale = self.originalSize[0]/self.picSize[0]
    
    def getSize(self):
        return self.originalSize

    def activity(self):
        self.root.bind('<Motion>', lambda event: self.onPic() if event.y <= self.picSize[1] else self.offPic())

    def onPic(self):
        self.canvas.config(cursor='pencil')
        self.root.bind('<Button-1>', self.increaseSeg)
    
    def offPic(self):
        self.canvas.config(cursor='')
        self.root.bind('<Button-1>',lambda x: None)

    def increaseSeg(self,event):
        self.segmentation.extend([event.x,event.y])
        self.realizePicSeg()
    
    def decreaseSeg(self,event):
        if len(self.segmentation) >= 2:
            self.segmentation = self.segmentation[:-2]
            self.realizePicSeg()
    
    def realizePicSeg(self):
        self.img = self.OGimg.copy()
        for seg in self.annotations:
            if len(seg) == 2:
                self.draw = ImageDraw.Draw(self.img)
                tmpList = [seg[0]-2,seg[1]-2] + [seg[0]+2,seg[1]+2]
                self.draw.ellipse(tmpList,fill=self.colors[self.color])
            elif len(seg) > 2:
                self.draw = ImageDraw.Draw(self.img)
                self.draw.line(seg,fill=self.colors[self.color],width=2)
        
        if len(self.segmentation) == 2:
            self.draw = ImageDraw.Draw(self.img)
            tmpList = [self.segmentation[0]-2,self.segmentation[1]-2] + [self.segmentation[0]+2,self.segmentation[1]+2]
            self.draw.ellipse(tmpList,fill=self.colors[self.color])
        elif len(self.segmentation) > 2:
            self.draw = ImageDraw.Draw(self.img)
            self.draw.line(self.segmentation,fill=self.colors[self.color],width=2)

        self.Tkimg = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(self.picSize[0]/2, self.picSize[1]/2, anchor="center", image=self.Tkimg)
        self.canvas.pack()
    
    def changeColor(self,event):
        self.color += 1
        self.color %= len(self.colors)
        self.realizePicSeg()

    def harvest(self,event):
        self.new(event)
        self.root.destroy()
    
    def restart(self,event):
        self.segmentation = []
        self.annotations = []
        self.realizePicSeg()

    def new(self,event):
        self.annotations.append(self.segmentation)
        self.segmentation = []
        self.realizePicSeg()
    
    def getInfo(self):
        if self.scale != 1.0:
            for seg in self.annotations:
                for i in range(len(self.segmentation)):
                    seg[i] *= self.scale
                    seg[i] = round(self.segmentation[i], 2)
        return self.annotations