import os
import tkinter as tk
from tkterminal import Terminal


class TerminalApp(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Create a vertical scrollbar
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a terminal widget
        self.terminal = Terminal(self, pady=5, padx=5,
                                 yscrollcommand=self.scrollbar.set)

        # Set the properties of the terminal
        self.terminal.config(
            borderwidth=2,
            cursor="xterm",
            exportselection=0,
            font=("Courier", 12),
            foreground="black",
            height=25,
            highlightbackground="blue",
            highlightcolor="blue",
            highlightthickness=1,
            insertbackground="blue",
            insertborderwidth=1,
            insertofftime=300,
            insertontime=600,
            insertwidth=2,
            relief="sunken",
            selectbackground="lightblue",
            selectborderwidth=1,
            spacing1=0,
            spacing2=0,
            spacing3=0,
            state="normal",
            tabs="1c",
            width=80,
            wrap="word",
        )

        # Pack the terminal widget
        self.terminal.pack(expand=True, fill='both')

        # Configure the terminal
        self.terminal.shell = True
        self.terminal.basename = os.getcwd()+">"

        # Bind Control + C to clear terminal
        self.terminal.bind("<Control-c>", lambda event: self.terminal.clear)
        self.terminal.bind("<Up>", self.get_last_command)

        # Configure terminal scrolling
        self.scrollbar.config(command=self.terminal.yview)

        # Set focus to the terminal
        self.terminal.focus_set()

    def get_last_command(self, event):
        # Retrieve the last command from the terminal
        last_command = self.terminal.get_last_command()
        # Do something with the last command, such as displaying it in the terminal
        if last_command is not None:
            # Insert the last command into the terminal
            self.terminal.insert(tk.END, last_command)


if __name__ == "__main__":
    root = tk.Tk()
    app = TerminalApp(master=root)
    app.mainloop()
