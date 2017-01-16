import tkinter as tk

class add_tag():
    def __init__(self, canvas):
        t = tk.Toplevel(canvas)
        t.wm_title("Add Tag")
        t.geometry("640x480+500+500")
        l = tk.Label(t, text="This is window #%s" % 1)
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

