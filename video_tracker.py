#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import file_item
import os
import sys
import io
import tkinter as tk
import sqlite3

class Application(tk.Frame):
    """Widget containing information about user-loaded videos."""
    table_name = 'video_table'
    tag_table = 'video_tags_table'
    t_ID = 'ID'
    t_filename = 'filename'
    t_cr_time = 'creation_time'
    t_file_hash = 'file_hash'
    t_columns = [t_cr_time, t_file_hash] # video tags added individually
    def __init__(self, master=None):
        # Initialize lists of data 
        self.vid_files  = [] # Representation of file data
        self.draw_depth = 0
        # Perform widget setup
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        # Load our stored database on startup
        self.db = sqlite3.connect('sql-videos.db')
        self.cursor = self.db.cursor()
        try:
            # Load the table of file information if it exists
            self.cursor.execute("SELECT * FROM {tn}".format(tn=self.table_name))
            data = self.cursor.fetchall()
            # Get the column names
            names = self.db.execute("SELECT * FROM {tn}"\
                                    .format(tn=self.tag_table))
            names = [nm[0] for nm in names.description]
#            print(names)
            for entry in data:
                # Find the value's twin in the tags table
#                print(entry)
                entry_idx = entry[0]
                fetch_cmd = "SELECT * FROM {tn} "\
                            "WHERE {idx}='{myid}';"\
                            .format(tn=self.tag_table, idx=self.t_ID,
                                    myid=entry_idx)
#                print(fetch_cmd)
                self.cursor.execute(fetch_cmd)
                rows = self.cursor.fetchall()
                tags = dict(zip(names, rows[0]))
#                print(tags)
                del tags['ID']
                
                vf = file_item.video_file(entry[1], self.res,
                                          self.restore_file_display,
                                          self.update_tag,
                                          fdatetime=entry[2],
                                          fhash=entry[3],
                                          tags=tags,
                                          table_index=entry[0])
                self.vid_files.append(vf)
                self.display_add_file(vf)
        except sqlite3.OperationalError:
            # If the table does not exist, create one
            try:
                self.cursor.execute("CREATE TABLE {tn} "\
                                    "({tid} INTEGER PRIMARY KEY AUTOINCREMENT,"\
                                    "{f} {ft})"\
                                    .format(tid=self.t_ID, tn=self.table_name,
                                            f=self.t_filename, ft='INTEGER'))
                self.db.commit()
                for t_col in self.t_columns:
                    self.cursor.execute("ALTER TABLE {tn} "\
                                        "ADD COLUMN '{cn}' {ct}"\
                                        .format(tn=self.table_name, cn=t_col,
                                                ct='TEXT'))
                self.cursor.execute("CREATE TABLE {tn} "\
                                    "({tid} INTEGER PRIMARY KEY)"\
                                    .format(tn=self.tag_table, tid=self.t_ID))
            except sqlite3.OperationalError:
                print("Something went wrong")
                print(sys.exc_info())
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
        self.e.bind('<KP_Enter>', self.search)
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
        vid_file = file_item.video_file(filepath, self.res,
                                        self.restore_file_display,
                                        self.update_tag, tags={})
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
    # Add data from the video file to our SQL database
    def update_stored_info(self, vid_file_info):
        # Insert a new record into the SQL database
        creation_time = str(vid_file_info.get_creation_time())
        file_hash = str(vid_file_info.get_hash())
        video_tags = vid_file_info.get_tags()
        filename = vid_file_info.get_filepath()
        insert_cmd = "INSERT INTO {tn} ({fn}, {cr}, {fh}) "\
                     "VALUES ('{mf}', '{tm}', '{mh}')"\
                     .format(tn=self.table_name, fn=self.t_filename,
                             cr=self.t_cr_time, fh=self.t_file_hash,
                             mf=filename, tm=creation_time,
                             mh=file_hash)
#        print(insert_cmd)
        self.cursor.execute(insert_cmd)
        self.db.commit()
        # Feed our table index back to the file
        fetch_cmd = "SELECT * FROM {tn} "\
                    "WHERE {fn}='{mf}' "\
                    "AND {fh}='{mh}';"\
                    .format(tn=self.table_name, fn=self.t_filename,
                            fh=self.t_file_hash, mf=filename, mh=file_hash)
        self.cursor.execute(fetch_cmd)
        rows = self.cursor.fetchall()
        if len(rows) > 1:
            print('More than one file matches the new addition, '\
                  'aborting...')
        else:
            idx = rows[0][0]
            vid_file_info.set_table_index(idx)
            # Insert a new line in the tags table for this table index
            insert_cmd = "INSERT INTO {tn} ({tid}) VALUES ({myid})"\
                         .format(tn=self.tag_table, tid=self.t_ID, myid=idx)
#            print(insert_cmd)
            self.cursor.execute(insert_cmd)
            self.db.commit()
    def update_tag(self, idx, tags):
        # tags should be a dictionary of format {tag: value}
#        print(tags)
        table_query = "PRAGMA table_info({tn})".format(tn=self.tag_table)
#        print(table_query)
        self.cursor.execute(table_query)
        columns = self.cursor.fetchall()
        columns = [row[1] for row in columns]
#        print(columns)
        for tag in tags:
            db_val = ",".join(tags[tag])
#            print(db_val)
            if tag not in columns:
                # create the column, allow for empty
                add_column = "ALTER TABLE {tn} ADD COLUMN '{cn}' TEXT"\
                             .format(tn=self.tag_table, cn=tag)
                self.cursor.execute(add_column)
            # insert the value for the appropriate entry
            update_cmd = "UPDATE {tn} SET {cn}=('{val}') WHERE {idx}={myid}"\
                         .format(tn=self.tag_table, cn=tag, val=db_val,
                                 idx=self.t_ID, myid=idx)
#            print(update_cmd)
            self.cursor.execute(update_cmd)
        self.db.commit()
    def display_add_file(self, vid_file_info):
        # Each file is given three lines of space
        # First line will be filename, then creation date
        # Second line will be tags
        self.draw_depth += vid_file_info.draw(self.draw_depth,
                                              self.restore_file_display)
        #print(vid_file_info.get_filename())

        # Update scroll region
        self.res.config(scrollregion=(0,0,300, self.draw_depth+5))
    def clear_file_display(self):
        """Clear all displayed objects."""
        for vid_file in self.vid_files:
            vid_file.hide()
        self.draw_depth = 0
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
