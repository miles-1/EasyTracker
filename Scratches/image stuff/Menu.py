import requests
from io import BytesIO
from PIL import Image
from MakeSeg import MakeSeg
from SeeSeg import SeeSeg
from cocoParse import getAnnotations, getCatsandMaxIDs, getIDs, getBBox, setImage
import tkinter
from tkinter import filedialog, messagebox
import sys
import os



class Section:
    def __init__(self,parts,root,position,option):
        self.parts = parts
        self.root = root
        self.option = option
        shift = [0,250,300,350,400]
        for indx in range(len(self.parts)):
            self.parts[indx].place((position[0],position[1]+shift[indx]),self.root)
        tkinter.Button(self.root,text="Start",command=self.getInfo).place(x=position[0],y=position[1]+350)
    
    def getInfo(self):
        answers = []
        for part in self.parts:
            answers.append(part.getInfo())
        if self.option == "check":
            self.runCheck(answers)
        elif self.option == "make":
            self.runMake(answers)

    def runCheck(self,answers):
        if answers[1] == "":
            messagebox.showwarning(message="You didn't select a COCO file. Please try again.")
            sys.exit(4)
        else:
            data = answers[1][1:]
        
        if answers[0] == "1":
            messagebox.showinfo(message="You didn't select a file or directory for pictures. It is assumed that you want to look thru all pictures by URL.")
            file_list = getIDs(data)
        elif answers[0][0] is "1":
            file_list = [answers[0][1:]]
        elif answers[0][0] is "2":
            file_list = [f for f in os.listdir(answers[0][1:])]
        
        self.root.destroy()
        
        for file_name in file_list:
            if file_name.isdigit():
                (annotations,url,name) = getAnnotations(data,iden=int(file_name))
                if url is not "":
                    response = requests.get(url)
                    img = Image.open(BytesIO(response.content))
                else:
                    messagebox.showwarning(message="Only use photo ID if it is a URL link. Otherwise, use the file name.")
                    sys.exit(5)
            else:
                (annotations,url,name) = getAnnotations(data,name=file_name)
                img = Image.open(file_name)

            self.root = tkinter.Tk()
            picture = SeeSeg(name,img,self.root,annotations)
            if picture.isLeave():
                break

    def runMake(self,answers):
        if answers[0] == "1":
            messagebox.showwarning(message="You didn't select a file or directory for a picture. Please try again.")
            sys.exit(6)
        if answers[1] == "":
            messagebox.showwarning(message="You didn't select a COCO file. Please try again.")
            sys.exit(7)
        
        (cats, maxPhotoID, maxAnnID) = getCatsandMaxIDs(answers[1][1:])

        if answers[2] == "":
            messagebox.showwarning(message="You didn't type a category name. Please try again.")
            sys.exit(8)
        elif answers[2][1:] not in cats:
            messagebox.showwarning(message="You didn't type a category name from the selected COCO file. Please try again.")
            sys.exit(9)
        
        cat = cats[answers[2][1:]] # category id for anything masked below

        self.root.destroy()

        if answers[0][0] is "1":
            file_list = [answers[0][1:]]
        elif answers[0][0] is "2":
            file_list = [f for f in os.listdir(answers[0][1:])]

        for file_name in file_list:
            if file_name[:4] == "http":
                response = requests.get(file_name)
                img = Image.open(BytesIO(response.content))
                name = file_name
                url = file_name

            else:
                img = Image.open(file_name)
                name = file_name
                url = ""

            self.root = tkinter.Tk()
            picture = MakeSeg(name,img,self.root)
            segmentation = picture.getInfo()
            size = picture.getSize()
            added = setImage(answers[1][1:],segmentation,cat,maxAnnID,size[0],size[1],name,url,maxPhotoID)  # adds annotation even if segmentation is empty
            if added:
                maxPhotoID += 1
            maxAnnID += 1


class DataChunk:
    def __init__(self,parts,check=""):
        self.check = check
        self.root = None
        self.parts = parts

    def place(self,position,root):
        shift = 0
        space = 50
        if self.check:
            self.check = tkinter.Checkbutton(root,text=self.check,command=self.changeActivity)
            self.check.place(x=position[0],y=position[1])
            shift = space
        self.parts[0].place((position[0],shift+position[1]),root)
        if len(self.parts) == 3:
            tkinter.Label(self.root,text="~or~",fg="#999999").place(x=position[0]+25,y=shift+0.5*space+position[1])
            self.parts[1].place((position[0],shift+space+position[1]),root)
            self.parts[2].place((position[0],shift+2*space+position[1]),root)

    def changeActivity(self):
        for parts in self.parts:
            parts.changeActivity()

    def getInfo(self):
        for parts in self.parts:
            result = parts.getInfo()
            if result == None or result == "":
                continue
            else:
                return result
        return ""


class DataPiece:
    def __init__(self,objType,words,active=True,isFile=True):
        self.words = words
        self.objType = objType
        self.active = active
        self.isFile = isFile
        self.filename = ""
        self.root = None
        self.label = None
        self.widget = None
        
    def place(self,position,root):
        self.root = root
        self.label = tkinter.Label(self.root,text=self.words)
        if self.objType == "f":  #filename button
            self.widget = tkinter.Button(self.root,text="pick file" if self.isFile else "pick folder",command=self.getFile)
        elif self.objType == "t":  #typing field
            self.widget = tkinter.Entry(self.root,width=10)

        self.label.place(x=position[0],y=position[1])
        self.widget.place(x=position[0] + 150,y=position[1])
        self.updateActivity()
    
    def getFile(self):
        if self.isFile:
            response = filedialog.askopenfilename()
            if isinstance(response, str):
                self.filename = "1" + response
        else:
            response = filedialog.askdirectory()
            if isinstance(response, str):
                self.filename = "2" + response
    
    def changeActivity(self):
        self.active = not self.active
        self.updateActivity()
    
    def updateActivity(self):
        if not self.active:
            self.label.config(fg="#cccccc")
            self.widget.config(state=tkinter.DISABLED)
        else:
            self.label.config(fg="black")
            self.widget.config(state=tkinter.NORMAL)
    
    def getInfo(self):
        if self.active:
            if isinstance(self.widget,tkinter.Button):
                return self.filename
            elif isinstance(self.widget,tkinter.Entry):
                return "1" + self.widget.get()
        else:
            return None