import tkinter as tk
from tkinter import simpledialog

from gitModule import generate_commit_message, push_changes

class CommitMessagePopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Commit Message")
        self.geometry("400x200")

        self.commit_message = tk.StringVar()

        label = tk.Label(self, text="Enter Commit Message:")
        label.pack(pady=5)

        self.commit_entry = tk.Entry(self, textvariable=self.commit_message, width=50)
        self.commit_entry.pack(pady=5)

        # Button to generate commit
        generate_button = tk.Button(self, text="Generate Commit", command=self.generate_commit)
        generate_button.pack(side=tk.LEFT, padx=10, pady=5)
        push_changes_button = tk.Button(self, text="Push Changes", command=self.push_changes)
        push_changes_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def generate_commit(self):
        # Generate the commit message here
        generated_message = generate_commit_message()
        print(generated_message)

        # Create a new popup to show the generated commit message
        popup = tk.Toplevel(self)
        popup.title("Generated Commit Message")
        popup.geometry("400x200")

        label = tk.Label(popup, text="Generated Commit Message:")
        label.pack(pady=5)

        # Wrap the commit message label inside the popup
        commit_label = tk.Label(popup, text=generated_message, wraplength=380)  # Adjust wraplength as needed
        commit_label.pack(pady=5)

        # Button to keep the commit message
        keep_button = tk.Button(popup, text="Keep", command=lambda: self.keep_commit(popup, generated_message))
        keep_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Button to discard the commit message
        discard_button = tk.Button(popup, text="Discard", command=popup.destroy)
        discard_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def keep_commit(self, popup, commit_message):
        # Update the commit message in the parent window's commit popup
        self.commit_entry.delete(0, tk.END)
        self.commit_entry.insert(tk.END, commit_message)
        popup.destroy()

    def push_changes(self):
        # Retrieve the commit message from the entry field
        commit_message = self.commit_message.get()

        # Logic to push changes goes here
        success, message = push_changes(commit_message)
        # Display a message indicating whether changes were successfully pushed or not
        result_popup = tk.Toplevel(self)
        result_popup.title("Push Changes Result")
        result_popup.geometry("300x300")
        result_label = tk.Label(result_popup, text=message, wraplength=380)
        result_label.pack(pady=20)

        if success:
            # If changes were successfully pushed, close the result popup after 2 seconds
            result_popup.after(2000, lambda: self.close_windows(result_popup))
        else:
            # If changes were not successfully pushed, keep the result popup open
            result_popup.lift()

    def close_windows(self, result_popup):
        # Destroy the main window and then the result popup
        self.destroy()
        

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    app = CommitMessagePopup(root)
    root.mainloop()
