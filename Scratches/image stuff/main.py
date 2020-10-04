from Menu import Section, DataChunk, DataPiece
import tkinter


def main():
    root = tkinter.Tk()

    canvas = tkinter.Canvas(root, width=700, height=550)
    tkinter.Label(root,text="Segmentation Program",font=("",24)).place(x=165, y=10)
    tkinter.Label(root,text="Check COCO Segmentation",font=("",12)).place(x=50, y=100)
    tkinter.Label(root,text="Make COCO Segmentation",font=("",12)).place(x=400, y=100)
    canvas.create_line(350,100,350,500)
    canvas.create_rectangle(40,140,310,340)
    canvas.create_rectangle(390,140,660,340)

    Section([DataChunk([DataPiece("f","file"),DataPiece("t","photo id"),DataPiece("f","folder",active=False,isFile=False)],check = "Check all pictures in directory"), DataChunk([DataPiece("f","COCO data")])], root, (50, 150),"check")
    Section([DataChunk([DataPiece("f","file"),DataPiece("t","photo url"),DataPiece("f","folder",active=False,isFile=False)],check = "Segment all pictures in directory"), DataChunk([DataPiece("f","COCO data")]), DataChunk([DataPiece("t","category")])], root, (400, 150),"make")

    canvas.pack()
    tkinter.mainloop()


main()