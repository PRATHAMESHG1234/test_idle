import tkinter as tk


class TextLineNumbers(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_widget = None
        self.config(state="disabled")

        # Configure the appearance of the line numbers
        self.config(
            background="lightgray",  # Background color
            foreground="black",       # Text color
            width=3 
            ,font=('Courier', 11)              # Width of the line number column
        )

    def attach(self, text_widget):
        self.text_widget = text_widget
        self.redraw()

        # Bind the <Configure> event to the redraw method
        self.text_widget.bind('<Configure>', self.redraw)
        self.text_widget.bind('<FocusIn>', self.redraw)
        self.text_widget.bind('<FocusOut>', self.redraw)
        # Bind MouseWheel event
        self.text_widget.bind('<MouseWheel>', self.redraw)
        # Bind text modification events
        self.text_widget.bind('<Key>', self.redraw)
        self.text_widget.bind('<Button-1>', self.redraw)
        self.text_widget.bind('<Button-3>', self.redraw)

    def redraw(self, event=None):
        self.config(state="normal", takefocus=0)
        last_line_index = self.text_widget.index("end-1c").split('.')[0]
        num_lines = int(last_line_index)
        line_numbers = '\n'.join(str(i) for i in range(1, num_lines + 1))
        self.delete("1.0", "end")
        self.insert("1.0", line_numbers)
        self.config(state="disabled")

    def on_configure(self, event):
        self.redraw()
        # Sync scrollbar with text widget
        self.yview_moveto(self.text_widget.yview()[0])

        # Update line numbers when the scrollbar is moved
