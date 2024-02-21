import os
import tkinter as tk
import tkinter.ttk as ttk
from PushChanges import CommitMessagePopup
from fileexplorer import FileExplorer
from terminal import TerminalApp
from text import TextLineNumbers
from app_methods import AppMethods
from PIL import Image, ImageTk

from visual import HTMLViewer


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("App with Sidebars")
        self.geometry("800x600")  # Initial size

        self.methods = AppMethods(self)
        self.active_open_file = ""
        self.tab_file_mapping = {}

        self.initialize_ui()

    def initialize_ui(self):

        self.setup_styles()  # Setup custom styles
        self.setup_navigation_bar()
        self.setup_sidebar_icons()
        self.setup_main_paned_window()
        self.open_default_file()
        self.bind_events()
        print(self.active_open_file)

    def open_default_file(self):
        # Get the list of files in the current working directory
        files = os.listdir(os.getcwd())

        # Custom logic to find and open the desired file
        for file in files:
            if os.path.isfile(file):
                # Here you can put your custom logic to determine which file to open
                if file.endswith('.py'):  # Example: Open the first .txt file found
                    file_path = os.path.join(os.getcwd(), file)

                    self.active_open_file = file
                    print(type(self.active_open_file))
                    with open(file_path, 'r') as file:
                        self.file_content = file.read()
                        self.file_text_editor.delete("1.0", tk.END)
                        self.file_text_editor.insert(tk.END, self.file_content)
                        self.line_numbers.redraw()
                    self.add_tab_to_notebook(self.active_open_file, file_path)

                    break

    def add_tab_to_notebook(self, file_name, file_path):
        tab_frame = ttk.Frame(self.opened_tabs_notebook)
        tab_frame.pack(fill=tk.X, expand=False)
        self.opened_tabs_notebook.add(tab_frame, text=file_name)

        # Map the tab name to its file path
        self.tab_file_mapping[file_name] = file_path

        # Bind the callback function to the NotebookTabChanged event
        self.opened_tabs_notebook.bind(
            "<<NotebookTabChanged>>", self.tab_changed_callback)

    def tab_changed_callback(self, event):
        selected_tab_index = event.widget.index("current")
        selected_tab_text = event.widget.tab(selected_tab_index, "text")

        # Open the file associated with the selected tab
        file_path = self.tab_file_mapping.get(selected_tab_text)
        if file_path:
            with open(file_path, 'r') as file:
                self.file_content = file.read()
                self.file_text_editor.delete("1.0", tk.END)
                self.file_text_editor.insert(tk.END, self.file_content)
                self.line_numbers.redraw()

    def setup_styles(self):
        self.style = ttk.Style()
        # self.style.configure('my.TPanedwindow', background='black')

    def setup_navigation_bar(self):

        self.nav_bar = ttk.Frame(self, height=50, style='TFrame')
        self.nav_bar.pack(side=tk.TOP, fill=tk.X)

        # Load and resize the app icon
        app_icon_image = Image.open(
            "../../assets/images/CustomTkinter_logo_single.png")
        app_icon_image = app_icon_image.resize(
            (32, 32), Image.LANCZOS)  # Adjust the size here
        app_icon_image = ImageTk.PhotoImage(app_icon_image)

        app_icon_label = tk.Label(self.nav_bar, image=app_icon_image,)
        # Keep a reference to prevent garbage collection
        app_icon_label.image = app_icon_image
        app_icon_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Navigation buttons
        nav_button_texts = ["Home", "Chat", "Add User", "Terminal"]
        for i, text in enumerate(nav_button_texts):
            button = ttk.Button(
                self.nav_bar, text=text,
                command=lambda idx=i: self.methods.handle_navigation_click(idx), style='TButton'
            )
            button.pack(side=tk.LEFT, padx=10, pady=5)

        push_code_button = tk.Button(
            self.nav_bar, text="Push Code", command=self.push_code_action, background='navy', foreground='white',
            activebackground='navy', activeforeground='white', borderwidth=5,
        )
        push_code_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Add Visualize Code button
        visualize_code_button = tk.Button(
            self.nav_bar, text="Visualize Code", command=self.visualize_code_action, background='navy', foreground='white',
            activebackground='navy', activeforeground='white', borderwidth=5
        )
        visualize_code_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def push_code_action(self):
        self.popup = CommitMessagePopup(self, self.active_open_file)
        self.popup.grab_set()
        self.wait_window(self.popup)

    def visualize_code_action(self):
        html_viewer = HTMLViewer(self.file_content)

    # Define the action for the Visualize Code button

    def setup_sidebar_icons(self):
        self.sidebar_icons = ttk.Frame(
            self, width=50, style='TFrame')
        self.sidebar_icons.pack(side=tk.LEFT, fill=tk.Y)

        icon_files = [
            "../../assets/images/home_dark.png",
            "../../assets/images/chat_dark.png",
            "../../assets/images/add_user_dark.png"
        ]
        self.icons = []
        for icon_file in icon_files:
            image = Image.open(icon_file)
            image = image.resize((32, 32), Image.LANCZOS)
            icon = ImageTk.PhotoImage(image)
            self.icons.append(icon)

        self.buttons = []
        for i, icon in enumerate(self.icons):
            button = ttk.Button(self.sidebar_icons, image=icon,
                                command=lambda idx=i: self.methods.toggle_sidebar(idx), padding=2, style='TButton')
            button.image = icon
            button.grid(row=i, column=0, pady=10, sticky="ew")
            self.buttons.append(button)

    def setup_main_paned_window(self):
        # Create the main PanedWindow
        self.main_paned_window = ttk.PanedWindow(
            self, orient=tk.VERTICAL, style="my.TPanedwindow")
        self.main_paned_window.pack(fill=tk.BOTH, expand=True)

        # Create the editor PanedWindow
        self.editor_paned_window = ttk.PanedWindow(
            self.main_paned_window, orient=tk.HORIZONTAL)
        self.main_paned_window.add(self.editor_paned_window, weight=1)

        # Create the explorer PanedWindow with VERTICAL orientation
        self.explorer_paned_window = ttk.PanedWindow(
            self.editor_paned_window, orient=tk.VERTICAL, style="my.TPanedwindow")
        self.editor_paned_window.add(self.explorer_paned_window, weight=1)

        # Create a PanedWindow for the FileExplorer
        self.file_explorer_paned_window = ttk.PanedWindow(
            self.explorer_paned_window, orient=tk.VERTICAL, style="my.TPanedwindow")
        self.explorer_paned_window.add(
            self.file_explorer_paned_window, weight=1)

        # Create the FileExplorer and add it to the self.file_explorer_paned_window
        self.sidebar_files = FileExplorer(
            self.file_explorer_paned_window,)
        self.file_explorer_paned_window.add(self.sidebar_files, weight=1)

        # Create the text PanedWindow
        self.text_paned_window = ttk.PanedWindow(
            self.editor_paned_window, orient=tk.HORIZONTAL, style="my.TPanedwindow")
        self.editor_paned_window.add(self.text_paned_window, weight=1)

        # Create the text editor frame
        self.text_editor_frame = ttk.Frame(
            self.text_paned_window, style='TFrame')
        self.text_paned_window.add(self.text_editor_frame, weight=0)

        self.opened_tabs_notebook = ttk.Notebook(self.text_editor_frame)
        self.opened_tabs_notebook.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Create a frame for the first tab
        first_tab_frame = ttk.Frame(self.opened_tabs_notebook)
        first_tab_frame.pack(fill=tk.X, expand=False)
        self.opened_tabs_notebook.add(
            first_tab_frame, text=self.active_open_file)

        # Create the text editor
        self.file_text_editor = tk.Text(self.text_editor_frame,
                                        #  bg='#2d2d2d',
                                        fg='black', insertbackground='#ddd',
                                        selectbackground='#444', selectforeground='#ddd', font=('Courier', 11))
        self.file_text_editor.pack(side="right", fill="both", expand=True)

        # Create the line numbers widget
        self.line_numbers = TextLineNumbers(
            self.text_editor_frame, width=1,
            #   bg='#2d2d2d'
            fg='#888')
        self.line_numbers.pack(side="left", fill="y")

        self.line_numbers.attach(self.file_text_editor)
        self.file_text_editor.bind(
            "<MouseWheel>", self.methods.scroll_text_and_update_line_numbers)

        # Create the terminal PanedWindow
        self.terminal_paned_window = ttk.PanedWindow(
            self.main_paned_window, orient=tk.HORIZONTAL)
        self.main_paned_window.add(self.terminal_paned_window, weight=10)

        # Create the Terminal widget
        self.terminal = TerminalApp(self.terminal_paned_window)
        self.terminal_paned_window.add(self.terminal, weight=5)
        self.terminal.place(x=0, y=0, relwidth=1, relheight=5)
        self.terminal_visible = True

        # Lift the navigation bar to the top
        self.nav_bar.lift()

    def bind_events(self):
        # Bind events
        self.bind('<Control-s>', lambda event: self.methods.save_file())
        self.sidebar_files.tree.bind('<Double-1>', self.methods.open_file)
        self.bind("<Configure>", self.methods.on_resize)


if __name__ == "__main__":
    app = App()
    app.mainloop()
