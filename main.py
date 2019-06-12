import tkinter as tk
from tkinter import *
from tkinter import font as tkfont
import os



cores = list()
M, alpha, lam, mu = [-1], [-1], [-1], [-1]


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, FirstInputs, SecondInputs):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        if page_name == "SecondInputs":
            name = SecondInputs.__name__
            frame = SecondInputs(parent=self.container, controller=self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Home Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Proceed to Simulation",
                            command=lambda: controller.show_frame("FirstInputs"))
        button2 = tk.Button(self, text="Exit",
                            command=controller.destroy)
        button1.pack()
        button2.pack()


class FirstInputs(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        Label(self, text="M").grid(row=1,
                                   column=1, sticky=W)
        Label(self, text="\u03BB").grid(row=2,
                                        column=1, sticky=W)
        Label(self, text="\u03B1").grid(row=3,
                                        column=1, sticky=W)
        Label(self, text="\u03BC").grid(row=4,
                                        column=1, sticky=W)

        # for taking inputs
        self.M = StringVar()
        Entry(self, textvariable=self.M,
              justify=RIGHT).grid(row=1, column=2)

        self.lam = StringVar()
        Entry(self, textvariable=self.lam,
              justify=RIGHT).grid(row=2, column=2)

        self.alpha = StringVar()
        Entry(self, textvariable=self.alpha,
              justify=RIGHT).grid(row=3, column=2)

        self.mu = StringVar()
        Entry(self, textvariable=self.mu,
              justify=RIGHT).grid(row=4, column=2)

        self.errorMessage = StringVar()
        error = Label(self, textvariable=
        self.errorMessage).grid(row=6,
                                column=2, sticky=E)

        # create the button
        btNextStep = Button(self, text="Next Step",
                            command=lambda: self.extract_params(controller)).grid(
            row=7, column=2, sticky=E)

    def extract_params(self, controller):
        try:
            print(self.M.get(), self.lam.get(), self.alpha.get(), self.mu.get())
            M[0] = int(self.M.get())
            lam[0] = float(self.lam.get())
            alpha[0] = float(self.alpha.get())
            mu[0] = float(self.mu.get())
            controller.show_frame("SecondInputs")
        except:
            self.errorMessage.set("Invalid or Empty Parameters")
            # controller.show_frame("SecondInputs")


class SecondInputs(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.cores = list()
        print(M[0], "********")
        for i in range(M[0]):
            Label(self, text="server " + str(i) + " cores").grid(row=i + 1, column=0)
            self.cores.append(StringVar())
            Entry(self, textvariable=self.cores[i]).grid(row=i + 1, column=1)

        self.errorMessage = StringVar()
        error = Label(self, textvariable=
        self.errorMessage).grid(row=M[0] + 2, column=1, sticky=E)

        button = tk.Button(self, text="Start Simulation",
                           command=lambda: self.extract_params(controller)).grid(row=M[0] + 3)

    def extract_params(self, controller):
        print(M[0], alpha[0], lam[0], mu[0])
        for i in range(M[0]):
            print(i, M)
            tmp = self.cores[i].get().split()
            try:
                assert len(tmp) > 1
                assert int(tmp[0]) + 1 == len(tmp)
                cores.append(list(map(float, tmp[1:])))
            except:
                self.errorMessage.set("Invalid or Empty Parameters")
                return
        print(cores)
        print(M[0], lam[0], alpha[0], mu[0])
        with open('gui_config.txt', 'w') as f:
            string = str(M[0]) + " " + str(lam[0]) + " " + str(alpha[0]) + " " + str(mu[0]) + "\n"
            f.write(string)
            for core in cores:
                f.write(str(len(core)) + " ")
                for param in core:
                    f.write(str(param) + " ")
                f.write("\n")
        simPath = os.getcwd() + "/simulation.py"
        os.system('python3 ' + simPath)
        controller.show_frame("StartPage")


if __name__ == "__main__":
    app = SampleApp(className=" Computer Simulation Project")
    app.geometry("400x300")
    app.mainloop()
