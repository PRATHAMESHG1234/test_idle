# app_methods.py
import tkinter as tk

import os


class AppMethods:
    def __init__(self, app_instance):
        self.app = app_instance

    def scroll_text_and_update_line_numbers(self, event):
        cur_view = self.app.file_text_editor.yview()
        self.app.file_text_editor.yview_scroll(-1 *
                                               (event.delta // 120), "units")
        self.app.line_numbers.yview_moveto(cur_view[0])

    def open_file(self, event):
        item_id = self.app.sidebar_files.tree.focus()
        if item_id:
            item_text = self.app.sidebar_files.tree.item(
                item_id, "text").strip()
            item_path = os.path.join(os.getcwd(), item_text)
            if os.path.isdir(item_path):
                self.open_files_in_directory(item_path)
            elif os.path.isfile(item_path):
                try:
                    self.app.add_tab_to_notebook(item_text,item_path) 
                    with open(item_path, 'r') as file:
                        self.app.file_content = file.read()
                        self.app.file_text_editor.delete("1.0", tk.END)
                        self.app.file_text_editor.insert(tk.END, self.app.file_content)
                        self.app.line_numbers.redraw()
                except OSError as e:
                    print(f"Failed to open file: {e}")

    def open_files_in_directory(self, directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                try:
                    with open(item_path, 'r') as file:
                        self.app.file_content = file.read()
                        self.app.file_text_editor.delete("1.0", tk.END)
                        self.app.file_text_editor.insert(tk.END, self.app.file_content)
                        self.app.line_numbers.redraw()
                        break
                except OSError as e:
                    print(f"Failed to open file: {e}")
            elif os.path.isdir(item_path):
                self.open_files_in_directory(item_path)
                break

    def save_file(self, event=None):
        content = self.app.file_text_editor.get("1.0", "end-1c")
        self.app.file_content = content
        selected_item = self.app.sidebar_files.tree.focus()
        if selected_item:
            file_name = self.app.sidebar_files.tree.item(
                selected_item, "text").strip()
            file_path = os.path.join(os.getcwd(), file_name)
            try:
                with open(file_path, 'w') as file:
                    file.write(content)
                print("File saved successfully.")
            except Exception as e:
                print(f"Error saving file: {e}")

    def toggle_sidebar(self, idx):
        if idx == 0:
            if self.app.file_explorer_visible:
                self.app.editor_paned_window.remove(self.app.sidebar_files)
                self.app.file_explorer_visible = False
            else:
                self.app.editor_paned_window.add(
                    self.app.sidebar_files, weight=1)
                self.app.file_explorer_visible = True
        elif idx == 2:
            if self.app.terminal_visible:
                self.app.main_paned_window.remove(
                    self.app.terminal_paned_window)
                self.app.terminal_visible = False
            else:
                self.app.main_paned_window.add(
                    self.app.terminal_paned_window, weight=1)
                self.app.terminal_visible = True

    def handle_navigation_click(self, idx):
        if idx == 0:
            pass
        elif idx == 1:
            pass
        elif idx == 2:
            pass
        elif idx == 3:
            if self.app.terminal_visible:
                self.app.main_paned_window.remove(
                    self.app.terminal_paned_window)
                self.app.terminal_visible = False
            else:
                self.app.main_paned_window.add(
                    self.app.terminal_paned_window, weight=1)
                self.app.terminal_visible = True

    def navigate(self, idx):
        pass

    def on_resize(self, event):
        pass
