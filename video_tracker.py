from mp4_parser import mp4_parser
import filename_parser
import os
import sys
import io
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
    def create_widgets(self):
        # Search bar
        self.search_fr = tk.Frame(self.master, borderwidth=1, relief=tk.RAISED)
        self.search_btn = tk.Button(self.search_fr) 
        self.search_btn['text'] = 'Search'
        self.search_btn['command'] = self.search
        self.search_btn.pack(side='right')
        self.e = tk.Entry(self.search_fr)
        self.e.delete(0, tk.END)
        self.e.insert(0, 'Enter search terms')
        self.e.bind('<Button-1>', self.clear_search)
        self.e.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_fr.pack(side=tk.TOP, fill=tk.X, expand=False)
        # List box
        self.filelist = []
        self.entry_list = tk.Frame(self.master, borderwidth=1, relief=tk.RAISED)
        self.results_str = tk.StringVar(self.master)
        self.results_str.set('Hello')
        self.res = tk.Canvas(self.entry_list, bg='blue')
##        self.res.create_line(0,0,200,100)
        self.res.pack(fill=tk.BOTH, expand=True)
##        self.results = tk.Label(self.entry_list, textvariable=self.results_str)
##        self.results.pack(fill=tk.BOTH)
        self.entry_list.pack(fill=tk.BOTH, expand=True)
        # Add Directory button
        # NOTE: Find a way to do this with just one window.
        self.add_dir = tk.Button(self.master, text='Add Directory',
                                 command=self.dir_selector)
        self.add_dir.pack(side='left')
        # Add Files... button
        self.add_files = tk.Button(self.master, text='Add Files...',
                                   command=self.file_selector)
        self.add_files.pack(side='left')
        # Quit button
        self.quit = tk.Button(self.master, text='Quit', fg='red',
                              command=self.master.destroy)
        self.quit.pack(side='right')
    def search(self):
        print('Searching...')
    def clear_search(self, event):
        self.e.delete(0, tk.END)
    def file_selector(self):
        filenames = tk.filedialog.askopenfilename(multiple=True)
        print(filenames)
        self.filelist.append(filenames)
        self.results_str.set(filenames)
    def dir_selector(self):
        filenames = tk.filedialog.askdirectory()
        print(filenames)
        self.filelist.append(filenames)
        self.results_str.set(filenames)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    root = tk.Tk()
    root.geometry("640x480+300+300")
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
