# Container for video files
# Standard Python libraries
import os
import errno
import datetime
import hashlib
import tkinter as tk
import subprocess
# Custom Python libraries
from mp4_parser import mp4_parser
import filename_parser
from tag_field import tag_field

# A video_file has a filepath, creation time (or best guess), a file hash
# (to verify if the file changes), last modification date, and dictionary of
# tags
class video_file(object):
    def __init__(self, filepath, canvas, redraw, width=615, font_size=15):
        self.version=0.1
        self.redraw = redraw
        # Clean up the filepath
        self.filepath = os.path.expanduser(filepath)
        # Verify the file exists
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT),
                                    self.filepath)
        filename = os.path.basename(self.filepath)
        # Gather available data about the file
        # For MP4 files, check for the creation date in the file
        metadata_info = None
        if os.path.splitext(filename)[-1].lower() == '.mp4':
            creation_secs = mp4_parser.findMp4Field(self.filepath,
                                                    'creation_time')
            metadata_info = datetime.datetime(1901, 1, 1)
            metadata_info += datetime.timedelta(seconds=creation_secs)
        file_dt = filename_parser.datetimeFromFilename(filename)
        if file_dt == datetime.datetime(1900, 1, 1, 0, 0, 0):
            if metadata_info:
                self.creation_time = metadata_info
            else:
                self.creation_time = None
        else:
            self.creation_time = file_dt
        self.file_hash = self.get_md5sum(self.filepath)
        self.video_tags = {'leads':['manfrommars', 'tom', 'dick', 'harry'],
                           'follows':['suzie', 'gladys', 'eunice'],
                           'event':['Rock That Swing Festival']}
        # Display elements
        # Arbitrary size for now
        self.size = 45
        self.width = width
        self.font_size = font_size
        self.canvas = canvas
        self.canvas_items = []
    def get_md5sum(self, filepath):
        hash_md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    def get_creation_time(self):
        return self.creation_time
    def get_hash(self):
        return self.file_hash
    def get_filename(self):
        return os.path.basename(self.filepath)
    def add_tag(self, tag, value):
        # Check to see if this is new
        if not tag in self.video_tags:
            self.video_tags[tag] = value
            self.redraw()
            return True
        else:
            #print('Tag [%s] exists: %s'%(tag, self.video_tags[tag]))
            return False
    def get_tags(self):
        return self.tags
    def draw(self, offset):
        self.canvas_items.append(
            self.canvas.create_text(4, offset,
                                 text=self.get_filename(),
                                 anchor=tk.NW, font=('Helvetica',
                                                     self.font_size),
                                 tag='title')
            )
        self.canvas_items.append(
            self.canvas.create_text(640-170, offset,
                                 text=self.get_creation_time(),
                                 anchor=tk.NW, font=('Helvetica',
                                                     self.font_size),
                                 tag='datetime')
            )
        self.tags = tag_field(self.canvas, offset, self.video_tags,
                              self.font_size, self.add_tag)
        self.size += self.tags.height_offset
        self.canvas_items.append(
            self.canvas.create_rectangle(0, offset, self.width,
                                      offset + self.size,
                                      outline='gray', fill='')
            )
        # Finally, bind to left mouse clicks
        for item in self.canvas_items:
            self.canvas.tag_bind(item, '<ButtonPress-1>', self.selected)
        return self.size
    def hide(self):
        for canvas_item in self.canvas_items:
            self.canvas.delete(canvas_item)
        self.size -= self.tags.height_offset
        self.tags.hide()
        self.canvas_items.clear()
    def selected(self, event):
        print('Selected: %s' % self.get_filename())
        # Use "find_overlapping" to get the bounding rectangle, which will be
        # the lowest numbered item
        rect = event.widget.find_closest(event.x, event.y)[0]
        local = [f for f in self.canvas.find_withtag('title')
                 if f in self.canvas_items]
        if rect in local:
            subprocess.Popen(['open', self.filepath])
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['canvas']
        del state['canvas_items']
        del state['tags']
        del state['size']
        del state['redraw']
        return state
    def __setstate__(self, state):
        self.__dict__=state
        self.__dict__['canvas_items'] = []
        self.__dict__['size'] = 45
