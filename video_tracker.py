from mp4_parser import mp4_parser
import file_item
import os
import sys
import io
import pickle
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        # Initialize lists of data 
        self.vid_files  = [] # Representation of file data
        self.file_texts = [] # Representation of displayed data
        self.data_file = 'videos.db'
        # Perform widget setup
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        # Load our stored database on startup
        if os.path.exists(self.data_file):
            # Load data
            with open(self.data_file, 'rb') as dbfile:
                try:
                    while True:
                        vid_file = pickle.load(dbfile)
                        self.vid_files.append(vid_file)
                        self.display_add_file(vid_file)
                except EOFError:
                    pass
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
        for f in filenames:
            self.add_filepath(f)
    def dir_selector(self):
        filenames = tk.filedialog.askdirectory()
        # Walk the directory and add all files
        for root, dirs, files in os.walk(filenames):
            for name in files:
                filepath = os.path.join(root, name)
                self.add_filepath(filepath)
    # Add a file at filepath to the list of files
    def add_filepath(self, filepath):
        if not os.path.exists(filepath):
            return None
        filename = os.path.basename(filepath)
        vid_file = file_item.video_file(filepath)
        # Check whether this file exists already
        for f in self.vid_files:
            if f.get_hash() == vid_file.get_hash():
                print('File already exists: %s' % vid_file.get_filename())
                return None
        # Update the database in memory
        self.vid_files.append(vid_file)
        # Add the file info to the display
        self.display_add_file(vid_file)
        # Update the database on the filesystem
        self.update_stored_info(vid_file)
        return vid_file
    # Add data from the video file to our pickeld database
    def update_stored_info(self, vid_file_info):
        with open(self.data_file, 'ab') as data_file:
            pickle.dump(vid_file_info, data_file)
    def display_add_file(self, vid_file_info):
        text_item = self.res.create_text(0, 15 * (len(self.vid_files)-1),
                                         text=vid_file_info.get_filename(),
                                         anchor=tk.NW,
                                         font=('Helvetica',15))
        self.file_texts.append(text_item)
        # Update scroll region
        self.res.config(scrollregion=(0,0,300, len(self.vid_files)*15))

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
