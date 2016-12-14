import file_item
import os
import sys
import io
import pickle
import tkinter as tk

class Application(tk.Frame):
    """Widget containing information about user-loaded videos."""
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
        self.e.bind('<Return>', self.search)
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
        self.res.bind_all('<MouseWheel>', self.vert_scroll)
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
        # For some reason, this is required to keep the first entry from being
        # cut off
        self.res.yview_scroll(10, 'units')
    def search(self, event=None):
        """Return the list of matching files."""
        #print('Searching...')
        val= self.e.get()
        #print(val)
        self.clear_file_display()
        for vidfile in self.vid_files:
            if val in vidfile.get_filename():
                #print(vidfile.get_filename())
                self.display_add_file(vidfile)
        #print(res)
    def clear_search(self, event):
        self.e.delete(0, tk.END)
        self.restore_file_display()
    def vert_scroll(self, event):
        self.res.yview_scroll(-1 * event.delta, 'units')
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
        # Each file is given three lines of space
        # First line will be filename, then creation date
        # Second line will be tags
        box_item = self.res.create_rectangle(0,
                                             45 * len(self.file_texts),
                                             615,
                                             45 * (len(self.file_texts) + 1),
                                             outline='gray')
        text_item = self.res.create_text(4, 45 * (len(self.file_texts)),
                                         text=vid_file_info.get_filename(),
                                         anchor=tk.NW,
                                         font=('Helvetica',15))
        date_item = self.res.create_text(640-170, 45 * (len(self.file_texts)),
                                         text=vid_file_info.get_creation_time(),
                                         anchor=tk.NW,
                                         font=('Helvetica',15))
        self.file_texts.append((text_item, box_item))
        #print(vid_file_info.get_filename())
        # Update scroll region
        self.res.config(scrollregion=(0,0,300, (len(self.file_texts))*45+5))
    def clear_file_display(self):
        """Clear all displayed objects."""
        for text in self.file_texts:
            self.res.delete(text[0])
            self.res.delete(text[1])
        self.file_texts = []
    def restore_file_display(self):
        """Restore all file objects to the Canvas."""
        self.clear_file_display()
        for vidfile in self.vid_files:
            self.display_add_file(vidfile)

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
