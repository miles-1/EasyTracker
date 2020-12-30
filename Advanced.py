import tkinter as tk


class Advanced:
    def __init__(self, root, canny_lower, canny_upper, kernel, dilate_it1, erode_it1,
                 dilate_it2, erode_it2, area_lower, area_upper):
        self.root = root
        self.canny_lower = canny_lower
        self.canny_upper = canny_upper
        self.kernel = kernel
        self.dilate_it1 = dilate_it1
        self.erode_it1 = erode_it1
        self.dilate_it2 = dilate_it2
        self.erode_it2 = erode_it2
        self.area_lower = area_lower
        self.area_upper = area_upper

        self.window = tk.Toplevel(self.root)
        self.l0 = tk.Label(self.window, text="Advanced - read 'Help' for more info", font=('Arial', 12))
        self.l1 = tk.Label(self.window, text="Canny Lower Level")
        self.l2 = tk.Label(self.window, text="Canny Upper Level")
        self.l3 = tk.Label(self.window, text="Kernel Size")
        self.l4 = tk.Label(self.window, text="Dilate Iterations 1")
        self.l5 = tk.Label(self.window, text="Erode Iterations 1")
        self.l6 = tk.Label(self.window, text="Dilate Iterations 2")
        self.l7 = tk.Label(self.window, text="Erode Iterations 2")
        self.l8 = tk.Label(self.window, text="Area Lower Bound")
        self.l9 = tk.Label(self.window, text="Area Upper Bound")
        labels = [self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8, self.l9]

        self.e1 = tk.Entry(self.window, width=5)
        self.e1.insert(0, str(self.canny_lower))
        self.e2 = tk.Entry(self.window, width=5)
        self.e2.insert(0, str(self.canny_upper))
        self.e3 = tk.Entry(self.window, width=5)
        self.e3.insert(0, str(self.kernel))
        self.e4 = tk.Entry(self.window, width=5)
        self.e4.insert(0, str(self.dilate_it1))
        self.e5 = tk.Entry(self.window, width=5)
        self.e5.insert(0, str(self.erode_it1))
        self.e6 = tk.Entry(self.window, width=5)
        self.e6.insert(0, str(self.dilate_it1))
        self.e7 = tk.Entry(self.window, width=5)
        self.e7.insert(0, str(self.erode_it1))
        self.e8 = tk.Entry(self.window, width=5)
        self.e8.insert(0, str(self.area_lower))
        self.e9 = tk.Entry(self.window, width=5)
        self.e9.insert(0, str(self.area_upper))
        entries = [self.e1, self.e2, self.e3, self.e4, self.e5, self.e6, self.e7, self.e8, self.e9]

        self.b0 = tk.Button(self.window, text="Set & Exit", command=self.exit)

        self.l0.grid(row=0, columnspan=2)
        for i in range(9):
            labels[i].grid(row=i+1, column=0)
            entries[i].grid(row=i+1, column=1)
        self.b0.grid(row=10, columnspan=2)

    def exit(self):
        self.canny_lower = int(self.e1.get())
        self.canny_upper = int(self.e2.get())
        self.kernel = int(self.e3.get())
        self.dilate_it1 = int(self.e4.get())
        self.erode_it1 = int(self.e5.get())
        self.dilate_it2 = int(self.e6.get())
        self.erode_it2 = int(self.e7.get())
        self.area_lower = int(self.e8.get())
        self.area_upper = int(self.e9.get())
        self.window.destroy()

    def getInfo(self):
        return self.canny_lower, self.canny_upper, self.kernel, self.dilate_it1, self.erode_it1, \
               self.dilate_it2, self.erode_it2, self.area_lower, self.area_upper
