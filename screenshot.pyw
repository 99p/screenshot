import tkinter as tk
import os.path
from PIL import ImageGrab
from datetime import datetime

desktop = os.path.expanduser("~/Desktop/")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry(f"{w}x{h}")
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-alpha", 0.2)
        self.canvas = tk.Canvas(self, width=w, height=h, bg='gray', highlightthickness=0)
        self.canvas.pack()
        self.b1 = self.bind('<Button-1>', self.rect_start)
        self.b3 = self.bind('<Button-3>', lambda e:self.destroy())
        self.bm = self.bind('<B1-Motion>', self.rect_motion)
        self.br = self.bind('<ButtonRelease-1>', self.rect_end)
        self.q = self.bind('q', lambda e: self.destroy())
        self.esc = self.bind('<Escape>', lambda e: self.destroy())

    def rect_start(self, e):
        self.startX = self.winfo_pointerx()
        self.startY = self.winfo_pointery()
        self.rect = self.canvas.create_rectangle(self.startX,self.startY,self.startX,self.startY, outline = "white", width=1)

    def rect_motion(self, e):
        self.canvas.delete(self.rect)
        self.endX = self.winfo_pointerx()
        self.endY = self.winfo_pointery()
        self.rect = self.canvas.create_rectangle(self.endX,self.endY,self.startX,self.startY, outline = "white", width=1)

    def rect_end(self, e):
        if abs(self.startX-self.endX) < 11 or abs(self.startY-self.endY) < 11:
            pass
        else:
            self.canvas.destroy()
            self.wm_attributes("-alpha", 0)
            self.img = ImageGrab.grab(bbox=(self.startX, self.startY, self.endX, self.endY))
            self.entry = tk.Entry(self, fg="black", bg="white", font="Calibri 40", relief=tk.FLAT)
            self.config(bg='white')
            self.wm_attributes("-alpha", .5)
            self.entry.insert(tk.END, datetime.now().strftime("%Y%m%d_%H%M%S"))
            self.entry.place(relx=.43, rely=.43)
            self.entry.focus_set()
            self.entry.select_range(0, tk.END)
            self.unbind('<ButtonPress-1>', self.b1)
            self.unbind('<B1-Motion>', self.bm)
            self.unbind('<ButtonRelease-1>', self.br)
            self.unbind('q', self.q)
            self.b1 = self.bind('<ButtonPress-1>', self.save_and_end)
            self.b3 = self.bind('<ButtonPress-3>', lambda e: self.destroy())
            self.bind('<Return>', self.save_and_end)

    def save_and_end(self, e):
        filename = self.entry.get()
        self.img.save(desktop + filename + ".png")
        self.destroy()



root = App()
root.mainloop()


