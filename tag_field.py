import tkinter as tk

class tag_field(object):
    # Fields:
    # canvas    the canvas to draw on
    # offset    vertical offset from the top to this entry
    # tags      dictionary of tags
    # font_size font size to print
    def __init__(self, canvas, offset, tags, font_size):
        self.canvas    = canvas
        self.offset    = offset
        self.tags      = tags
        self.font_size = font_size
        # Starting position of tag field
        self.x = 4
        self.y = 20
        for tag in tags:
            self.rounded_box = rounded_box(self.canvas, tag,
                                           self.offset, self.font_size,
                                           self.x, self.y)
    def hide(self):
        self.rounded_box.hide()

class rounded_box(object):
    def __init__(self, canvas, tag, offset, font_size, x, y):
        self.canvas_items = []
        self.canvas = canvas
        self.font_size = font_size
        self.length = tk.font.Font(family='Helvetica',
                                   size=self.font_size).measure(tag)
        
        self.canvas_items.append(
            self.canvas.create_arc(4, offset+30, 14, offset+20,
                                   start=90, extent=90,
                                   fill="gray", outline='',
                                   style=tk.PIESLICE)
            )
        self.canvas_items.append(
            self.canvas.create_arc(4+self.length, offset+30,
                                   14+self.length, offset+20,
                                   start=0, extent=90,
                                   fill="gray", outline='',
                                   style=tk.PIESLICE)
            )
        self.canvas_items.append(
            self.canvas.create_arc(4, offset+26+self.font_size,
                                   14, offset+16+self.font_size,
                                   start=180, extent=90,
                                   fill="gray", outline='',
                                   style=tk.PIESLICE)
            )
        self.canvas_items.append(
            self.canvas.create_arc(4+self.length, offset+26+self.font_size,
                                   14+self.length, offset+16+self.font_size,
                                   start=270, extent=90,
                                   fill="gray", outline='',
                                   style=tk.PIESLICE)
            )
        self.canvas_items.append(
            self.canvas.create_rectangle(4, offset+25,
                                         14+self.length,
                                      offset + 21+self.font_size,
                                      outline='gray', fill='gray')
            )
        self.canvas_items.append(
            self.canvas.create_rectangle(9, offset+20,
                                         9+self.length,
                                      offset + 26+self.font_size,
                                      outline='gray', fill='gray')
            )
        self.canvas_items.append(
            self.canvas.create_text(9, offset+7+self.font_size,
                                 text=tag,
                                 anchor=tk.NW, font=('Helvetica',
                                                     self.font_size),
                                 tag='datetime')
            )
        
    def hide(self):
        for canvas_item in self.canvas_items:
            self.canvas.delete(canvas_item)
        self.canvas_items.clear()
