import tkinter as tk
import webview
from urllib.parse import quote

class HTMLViewer(tk.Toplevel):
    def __init__(self, code):
        super().__init__()
        self.encoded_code = quote(code)  # Encode the code parameter
        self.title("HTML Viewer")
        self.geometry("800x800")

        # Create a webview window
        self.webview = webview.create_window(
            "Browser", f"http://pythontutor.com/iframe-embed.html#code={self.encoded_code}&origin=opt-frontend.js&cumulative=false&heapPrimitives=false&textReferences=false&py=3&rawInputLstJSON=%5B%5D&curInstr=0")
        webview.start()
