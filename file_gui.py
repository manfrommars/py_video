# Container for the graphical display elements of a video file
import tkinter as tk
#import file_item

class video_widget(object):
    size = 0
    def __init__(self, canvas, binding, item, width=615, font_size=15):
        # Arbitrary size for now
        self.size = 45
        self.width = width
        self.font_size = font_size
        self.binding = binding
        self.canvas = canvas
        self.item = item
        self.canvas_items = []
        # Draw on the canvas upon creation
        self.draw()

    def draw(self, offset):
        self.canvas_items.append(
            self.canvas.create_rectangle(0, self.offset, self.width,
                                      self.offset + self.size,
                                      outline='gray', fill='white')
            )
        self.canvas_items.append(
            self.canvas.create_text(4, self.offset,
                                 text=self.item.get_filename(),
                                 anchor=tk.NW, font=('Helvetica',
                                                     self.font_size))
            )
        self.canvas_items.append(
            self.canvas.create_text(640-170, self.offset,
                                 text=self.item.get_creation_time(),
                                 anchor=tk.NW, font=('Helvetica',
                                                     self.font_size))
            )
        # Finally, bind to left mouse clicks
        for item in self.canvas_items:
            self.canvas.tag_bind(item, '<ButtonPress-1>', self.binding)
        return self.size
    def hide(self):
        for canvas_item in self.canvas_items:
            self.canvas.delete(canvas_item)
        self.canvas_items.clear()
