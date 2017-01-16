import tkinter as tk
import add_tag

class tag_field(object):
    # Fields:
    # canvas    the canvas to draw on
    # offset    vertical offset from the top to this entry
    # tags      dictionary of tags
    # font_size font size to print
    def __init__(self, canvas, offset, tags, font_size):
        self.canvas        = canvas
        self.offset        = offset
        self.tags          = tags
        self.font_size     = font_size
        self.height_offset = 0
        self.tag_boxes     = []
        # Starting position of tag field
        self.x = 4
        self.y = 10
        # Iterate over the list of tags
        for key in tags:
            # Each key should have at least one value in a list
            if len(tags[key]) < 1:
                print('Error, key \'%s\' invalid' % key)
                continue
            tag = '%s: ' % key
            for val in tags[key]:
                if val == tags[key][-1]:
                    tag += ' %s' % val
                else:
                    tag += ' %s,' % val
            length = tk.font.Font(family='Helvetica',
                                  size=self.font_size).measure(tag)
            # Determine if this tag will fit
            # if x == 4, at start nothing we can do
            # otherwise, if x + length is greater than the size of the window,
            # increase y
            if self.x + length > 640:
                self.x = 4
                self.y += 24
                self.height_offset += 24
            self.tag_boxes.append(rounded_box(self.canvas, tag,
                                           self.offset, self.font_size,
                                           self.x, self.y, length))
            self.x += length + 14
        # Add tag
        length = tk.font.Font(family='Helvetica',
                              size=self.font_size).measure("Add tag")
        self.btn = rounded_button(self.canvas, "Add tag",
                                           self.offset, self.font_size,
                                           self.x, self.y, length)
        # newtagbtn = add_tag.add_tag(self.canvas)
    def hide(self):
        for box in self.tag_boxes:
            box.hide()
        self.height_offset = 0

class rounded_box(object):
    def __init__(self, canvas, tag, offset, font_size, x, y, length,
                 color="gray"):
        self.canvas_items = []
        self.canvas = canvas
        self.font_size = font_size
        
        self.canvas_items.append(
            self.canvas.create_arc(x+0 , offset+y+20,
                                   x+10, offset+y+10,
                                   start=90, extent=90,
                                   fill=color, outline='',
                                   style=tk.PIESLICE)
            )
        self.canvas_items.append(
            self.canvas.create_arc(x+0 +length, offset+y+20,
                                   x+10+length, offset+y+10,
                                   start=0, extent=90,
                                   fill=color, outline='',
                                   style=tk.PIESLICE)
            )
        self.canvas_items.append(
            self.canvas.create_arc(x+0 , offset+y+16+self.font_size,
                                   x+10, offset+y+6 +self.font_size,
                                   start=180, extent=90,
                                   fill=color, outline='',
                                   style=tk.PIESLICE)
            )
        self.canvas_items.append(
            self.canvas.create_arc(x+0 +length, offset+y+16+self.font_size,
                                   x+10+length, offset+y+6 +self.font_size,
                                   start=270, extent=90,
                                   fill=color, outline='',
                                   style=tk.PIESLICE)
            )
        self.canvas_items.append(
            self.canvas.create_rectangle(x+0,
                                             offset+y+15,
                                         x+10+length,
                                             offset+y+11+self.font_size,
                                         outline=color, fill=color)
            )
        self.canvas_items.append(
            self.canvas.create_rectangle(x+5,
                                             offset+y+10,
                                         x+5+length,
                                             offset+y+16+self.font_size,
                                         outline=color, fill=color)
            )
        self.canvas_items.append(
            self.canvas.create_text(x+5, offset+y-3+self.font_size,
                                    text=tag,
                                    anchor=tk.NW, font=('Helvetica',
                                                        self.font_size),
                                    tag='datetime')
            )
        
    def hide(self):
        for canvas_item in self.canvas_items:
            self.canvas.delete(canvas_item)
        self.canvas_items.clear()

class rounded_button(rounded_box):
    def __init__(self, canvas, tag, offset, font_size, x, y, length):
        rounded_box.__init__(self, canvas, tag, offset, font_size, x, y, length,
                             "slate gray")
        for item in self.canvas_items:
            self.canvas.tag_bind(item, '<Button-1>', self.button_select)
    def button_select(self, event=None):
        add_tag.add_tag(self.canvas)
