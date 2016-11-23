from mp4_parser import mp4_parser
import filename_parser
import os
import sys
import io
import tkinter as tk

def old_fn():
    stdout_redirect = 'file_output.txt'

    with open(stdout_redirect, 'w') as f:
        sys.stdout = f

        dirpath = '~/Movies/dance_tutorials/'
        dirpath = os.path.expanduser(dirpath)
        mp4_parser.DEBUG=0
        print("Run parser:")

    ##    root = "~/Movies/dance_tutorials/spain_videos_miguel/"
    ##    for i in range(0,1):
    ##        for filename in ["9-3-2015.mp4"]:
        for root, directories, filenames in os.walk(dirpath):
            for filename in filenames:
                path = os.path.join(root,filename)
                print(path.encode('utf-8'))
                if path.endswith('.mp4'):
                    print(path.encode('utf-8'))
                    #print('='*60)
                    #mp4_parser.readMp4File(os.path.join(root,filename))
                    #print('='*60)
                    #field = 'creation_time'
                    #val = mp4_parser.findMp4Field(os.path.join(root,filename), field)
                    #print("DEBUG: " + field + "="+ str(val))
                    date = filename_parser.datetimeFromFilename(filename)
                    print(str(date))
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
        self.entry_list = tk.Frame(self.master, borderwidth=1, relief=tk.RAISED)
        self.results = tk.Label(self.entry_list, text='Hello')
        self.results.pack(fill=tk.BOTH)
        self.entry_list.pack(fill=tk.BOTH, expand=True)
        # Quit button
        self.quit = tk.Button(self.master, text='Quit', fg='red',
                              command=self.master.destroy)
        self.quit.pack(side='right')
    def search(self):
        print('Searching...')
    def clear_search(self, event):
        self.e.delete(0, tk.END)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    root = tk.Tk()
    root.geometry("300x200+300+300")
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
