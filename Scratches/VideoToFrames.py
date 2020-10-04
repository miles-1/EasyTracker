import cv2
import sys
import os
from tkinter import Tk, filedialog

done = False
root = Tk()
root.withdraw()

line = "\n" + "-"*50 + "\n"

menu = "\nWhat would you like to do? Type a number.\n\t1) Convert picture to frames\n\t2) Convert frames to differences\n\t\
3) Put outline on original objects\n\t0) Quit"

menu1 = "What number of frames per second do you want to extract?\nPress enter to extract all: "

while not done:
    print(menu)
    response = int(input("Response: "))
    os.system('cls||clear')

    if response == 1:
        print("Select File.")
        file_name = filedialog.askopenfilename()
        video = cv2.VideoCapture(file_name)
        os.system('cls||clear')
        temp = input(menu1)

        progress, frame = video.read()
        (i, frameCount) = (0, 0)
        fps = video.get(cv2.CAP_PROP_FPS)
        ratio = int(fps // int(temp)) if temp else 1
        lengthOfVid = int(video.get(cv2.CAP_PROP_FRAME_COUNT) // ratio)

        print(f"{lengthOfVid} frames to convert for {file_name}.\nVideo fps: {fps}. Ratio of frames extracted per total: {ratio}.")
        print("Please wait...")
        #sys.stdout.flush()
        
        folder_name = file_name[:file_name.rfind(".")] + " sequence"
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        
        if len(str(lengthOfVid)) < len(str(lengthOfVid + 5)):
            lengthOfVid = lengthOfVid + 5

        form = "0>" + str(len(str(lengthOfVid)))

        while progress:
            if i % ratio == 0:
                cv2.imwrite(f"{folder_name}/{round(ratio/fps,2)}sec-image{format(frameCount, form)}.jpg", cv2.UMat(frame))
                frameCount += 1
            i += 1
            progress, frame = video.read()
            if i % (ratio * 100) == 0:
                print(f"\n{format(frameCount, form)} frames done ", end="", flush=True)
            elif i % (ratio * 10) == 0:
                print("*", end="", flush=True)
            elif i == 1:
                print(f"{format(frameCount, form)} frame  done ", end="", flush=True)

        video.release()

        os.system('cls||clear')

        print(f"Process complete. Saved to {folder_name}.",line)
    
    elif response == 2:
        # TODO: this thing
        pass
    
    elif response == 3:
        # TODO: this thing
        pass

    elif response == 0:
        done = True

root.destroy()


# img.getbbox() is none if img is totally black
# same with img.convert("L").getextrema() == (0,0), which might be faster.
