import tkinter as tk
from tkinter import ttk
import pandas as pd
from my_catboost.catboost_classifier import CatBoostAnalyzer as CBA

class DataInputGUI:

    def __init__(self, root):
        self.root = root
        
        cba = CBA()
        cba.test()
        cba.prod()
        text=cba.get_text()
        win = tk.Toplevel(self.root)
        win.title("Résultat")
        win.geometry("600x400")

        frame = ttk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(
            frame,
            wrap="word",
            yscrollcommand=scrollbar.set,
            font=("Arial", 10)
        )
        text_widget.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=text_widget.yview)

        text_widget.insert("1.0", text)
        text_widget.config(state="disabled")
    
    
    
    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    app = DataInputGUI(root)
    app.run()


if __name__ == "__main__":
    main()
