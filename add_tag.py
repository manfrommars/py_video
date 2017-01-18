import tkinter as tk

class add_tag():
    def __init__(self, canvas, tags):
        self.tags = tags
        self.tag_texts = []
        # Create popup window for entering tags
        self.t = tk.Toplevel(canvas)
        self.t.wm_title("Edit Tags")
        self.t.geometry("+500+500")
        # [ Key  | Value       | Add Tag ]
        self.fr1 = tk.Frame(self.t, borderwidth=1, relief=tk.RAISED)
        self.tag_key = tk.Entry(self.fr1)
        self.tag_key.delete(0, tk.END)
        self.tag_key.insert(0, 'Key')
        self.tag_key.bind('<Button-1>', self.clear_key)
        self.tag_value = tk.Entry(self.fr1, width=60)
        self.tag_value.delete(0, tk.END)
        self.tag_value.insert(0, 'Tag Value')
        self.tag_value.bind('<Button-1>', self.clear_value)
        self.tag_btn = tk.Button(self.fr1, text='Add Tag', command=self.tag_btn)
        self.tag_key.pack(side='left')
        self.tag_btn.pack(side='right')
        self.tag_value.pack(side='left', fill=tk.X, expand=True)
        self.fr1.pack(side=tk.TOP, fill=tk.X, expand=False)
        # Below, add a list of all current tags.  The goal is for them to be
        # selectable, so make each key:value pair its own item
        for key in self.tags:
            text = '%s:' % key
            for val in self.tags[key]:
                if val == self.tags[key][-1]:
                    text += ' %s' % val
                else:
                    text += ' %s,' % val
            self.tag_texts.append(tk.Label(self.t, text=text, justify=tk.LEFT,
                                           anchor=tk.W))
            self.tag_texts[-1].pack(fill=tk.X, expand=False, padx=10)
    def tag_btn(self, event=None):
        key = self.tag_key.get()
        val = self.tag_value.get()
        print('Key \'%s\' Value \'%s\'' % (key, val))
        # When the user adds a key:value pair, check for NULL strings and the
        # default values
        BAD_KEYS = ['Key', '']
        BAD_VALUES = ['Tag Value', '']
        if key in BAD_KEYS or val in BAD_VALUES:
            return
        # Parse values for valid strings
        print(val)
        vallist = val.split(',')
        print(vallist)
        # add the key:value to the local listing
        self.tags[key] = vallist
        text = '%s:' % key
        for val in self.tags[key]:
            if val == self.tags[key][-1]:
                text += ' %s' % val
            else:
                text += ' %s,' % val
        self.tag_texts.append(tk.Label(self.t, text=text, justify=tk.LEFT,
                                       anchor=tk.W))
        self.tag_texts[-1].pack(fill=tk.X, expand=False, padx=10)
    def clear_key(self, event=None):
        self.tag_key.delete(0, tk.END)
    def clear_value(self, event=None):
        self.tag_value.delete(0, tk.END)
