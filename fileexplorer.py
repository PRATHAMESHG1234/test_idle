import os
import tkinter as tk
from tkinter import ttk

from gitModule import get_commit_history, check_git_repository


class FileExplorer(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Create custom style
        custom_style = ttk.Style()

        # Configure Treeview style
        custom_style.configure(
            'Custom.Treeview',
            foreground='black'
        )

        self.repo = check_git_repository()

        # Configure Frame style for the timeline
        custom_style.configure(
            'Custom.TFrame',
            highlightbackground="blue", highlightcolor="blue", highlightthickness=5,
            foreground='blue'
        )

        # Create Treeview widget
        self.tree = ttk.Treeview(self, style='Custom.Treeview')
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Define icons for folders and files
        self.folder_icon = tk.PhotoImage(
            file="../../assets/images/folder_icon.PNG").subsample(22, 22)
        self.file_icon = tk.PhotoImage(
            file="../../assets/images/file_icon.png").subsample(22, 22)

        # Bind double click event to handle folder opening
        self.tree.bind('<Double-1>', self.on_double_click)

        # Populate tree with current directory contents
        self.populate_tree()

        # Create the timeline frame
        self.timeline_frame = ttk.Frame(
            self, style='Custom.TFrame',  relief=tk.SOLID,)

        texts = get_commit_history(self.repo)
        self.options_visible = False
        self.selected_option = tk.StringVar()
        self.selected_option.set(" ▶ " + " Timeline")

        self.selected_option_label = ttk.Label(
            self.timeline_frame, textvariable=self.selected_option,
            foreground="black", anchor="w", cursor="hand2")
        self.selected_option_label.pack(
            side=tk.TOP, fill=tk.X, pady=5)
        self.selected_option_label.bind(
            "<Button-1>", lambda event: self.toggle_options())

        self.dropdown_options_frame = ttk.Frame(
            self.timeline_frame, style='Custom.TFrame')

        self.dropdown_options_canvas = tk.Canvas(
            self.dropdown_options_frame)
        self.dropdown_options_frame.bind(
            "<Configure>", lambda e: self.configure_dropdown_canvas())

        self.dropdown_options_scrollbar = ttk.Scrollbar(
            self.dropdown_options_frame, orient="vertical", command=self.dropdown_options_canvas.yview)
        self.dropdown_options_scrollable_frame = ttk.Frame(
            self.dropdown_options_canvas)

        self.dropdown_options_canvas.create_window(
            (0, 0), window=self.dropdown_options_scrollable_frame, anchor="nw")
        self.dropdown_options_canvas.configure(
            yscrollcommand=self.dropdown_options_scrollbar.set)

        for text in texts:
            # Create a frame for each option to hold the border
            option_frame = ttk.Frame(
                self.dropdown_options_scrollable_frame, borderwidth=1, relief="solid")
            option_frame.pack(side=tk.TOP, fill=tk.X)

            # Create a label inside the frame with the text
            option_label = ttk.Label(
                option_frame, text=text, anchor="w", cursor="hand2", wraplength=300,
                foreground=""
            )
            option_label.pack(side=tk.TOP, fill=tk.X,
                              padx=10, pady=(2, 2))
            option_label.bind(
                "<Button-1>", lambda event, text=text: self.select_option(text))

        self.dropdown_options_canvas.pack(
            side="left", fill="both", expand=True)

        self.dropdown_options_scrollbar.pack(side="right", fill="y")
        self.dropdown_options_frame.pack_forget()

        self.timeline_frame.pack(side=tk.BOTTOM, fill=tk.X)

    def configure_dropdown_canvas(self):
        self.dropdown_options_canvas.config(
            scrollregion=self.dropdown_options_canvas.bbox("all"))
        self.dropdown_options_canvas.config(
            width=self.dropdown_options_frame.winfo_width())

    def toggle_options(self):
        if self.options_visible:
            self.dropdown_options_frame.pack_forget()
            self.selected_option.set(" ▶ Timeline")
        else:
            self.dropdown_options_frame.pack(
                side=tk.TOP, fill=tk.X, expand=True)
            self.selected_option.set(" ▼ Timeline")
        self.options_visible = not self.options_visible

    def select_option(self, option):
        self.selected_option.set(option)
        self.toggle_options()

    def populate_tree(self, path="."):
        # Clear existing items in the tree
        self.tree.delete(*self.tree.get_children())

        # Populate the tree recursively
        self._populate_tree(path)

    def _populate_tree(self, path, parent=""):
        # Get list of items (files and directories) in the given path
        items = os.listdir(path)

        # Iterate through items and insert into tree
        for item in items:
            item_path = os.path.join(path, item)
            item_type = "folder" if os.path.isdir(
                item_path) else "file"

            # Insert item with appropriate icon
            if parent:
                if item_type == "folder":
                    item_id = self.tree.insert(
                        parent, "end", text=f" {item}", tags=("folder",), image=self.folder_icon)
                else:
                    item_id = self.tree.insert(
                        parent, "end", text=f" {item}", tags=("file",), image=self.file_icon)
            else:
                if item_type == "folder":
                    item_id = self.tree.insert(
                        "", "end", text=f" {item}", tags=("folder",), image=self.folder_icon)
                else:
                    item_id = self.tree.insert(
                        "", "end", text=f" {item}", tags=("file",), image=self.file_icon)

            # Recursively populate subdirectories
            if os.path.isdir(item_path):
                self._populate_tree(item_path, item_id)

    def on_double_click(self, event):
        # Get the selected item in the tree
        item_id = self.tree.focus()
        if item_id:
            item_text = self.tree.item(item_id, "text")
            item_path = os.path.join(os.getcwd(), item_text)

            # Open folder if it's a directory
            if os.path.isdir(item_path):
                self.populate_tree(item_path)


# Sample usage
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")

    file_explorer = FileExplorer(root)
    file_explorer.pack(fill=tk.BOTH, expand=True)

    # Update the tree view after creating a new file
    # Example: If new_file.txt is created, call populate_tree again
    # file_explorer.populate_tree()

    root.mainloop()
