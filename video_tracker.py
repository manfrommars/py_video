from mp4_parser import mp4_parser
import file_item
import os
import sys
import io
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        self.vid_files = []
        self.filelist = []
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
    def create_widgets(self):
        # Search bar
        self.search_fr = tk.Frame(self.master, borderwidth=1,
                                  relief=tk.RAISED)
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
        
        # Videos listed in a scrollable canvas
        self.entry_list = tk.Frame(self.master, borderwidth=1,
                                   relief=tk.RAISED)
        self.res = tk.Canvas(self.entry_list)
        self.ybar = tk.Scrollbar(self.entry_list, orient=tk.VERTICAL)
        self.ybar.pack(side=tk.RIGHT, fill=tk.Y)
        self.ybar.config(command=self.res.yview)
        self.res.config(yscrollcommand=self.ybar.set)
        self.res.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
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
        for f in filenames:
            self.vid_files.append(file_item.video_file(f))
        self.filelist.append(filenames)
##        self.results_str.set(filenames)
    def dir_selector(self):
        filenames = tk.filedialog.askdirectory()
        # Walk the directory and add all files
        for root, dirs, files in os.walk(filenames):
            for name in files:
                filepath = os.path.join(root, name)
                self.vid_files.append(file_item.video_file(filepath))
                self.filelist.append(filepath)
##                self.w = tk.Canvas(self.res, height=20)
##                self.w.create_text(200,10,text=filepath)
##                self.w.pack(fill=tk.X)
                self.res.create_text(200, 15 * (len(self.filelist)-1) + 5, text=filepath)
        print(self.filelist)
        self.res.config(scrollregion=(0,0,300, len(self.filelist)*15))
##        self.results_str.set(self.filelist)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    root = tk.Tk()
    root.title('Video Tracker')
    root.geometry("640x480+300+300")
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
