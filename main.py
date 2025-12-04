import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os


class MainMenu:
    
    def __init__(self, root):
        # def object initialization
        self.root = root
        self.root.title("Mushroom AI - Main Menu")
        self.root.geometry("500x500")
        
        # to get this rep and the others .py to execute
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # create the frame and param visuals
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        title_label = ttk.Label(main_frame, text="Mushroom AI", font=("Arial", 18, "bold"))
        title_label.pack(pady=20)
        subtitle_label = ttk.Label(main_frame, text="Select an application", font=("Arial", 10))
        subtitle_label.pack(pady=10)
        
        # button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # buttons setup
        self.display_btn = ttk.Button(button_frame, text="Display Data & Parameters", command=self.launch_display_app)
        self.display_btn.pack(fill=tk.X, pady=10, ipady=15)
        self.input_btn = ttk.Button(button_frame, text="User Input Form", command=self.launch_input_app)
        self.input_btn.pack(fill=tk.X, pady=10, ipady=15)
        self.exit_btn = ttk.Button(button_frame, text="Exit", command=self.root.quit)
        self.exit_btn.pack(fill=tk.X, pady=10, ipady=15)
        
        # status bar
        self.status_label = ttk.Label(main_frame, text="Ready", font=("Arial", 8), foreground="gray")
        self.status_label.pack(side=tk.BOTTOM, pady=10)
    
    # function applied to button display
    def launch_display_app(self):
        self.update_status("Launching display app...")
        try:
            display_file = os.path.join(self.script_dir, "gui_display.py")
            if os.path.exists(display_file):
                subprocess.Popen([sys.executable, display_file])
            else:
                self.update_status("Error: gui_display.py not found")
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
    
    # function applied to button input
    def launch_input_app(self):
        self.update_status("Launching input form...")
        try:
            input_file = os.path.join(self.script_dir, "input_form.py")
            if os.path.exists(input_file):
                subprocess.Popen([sys.executable, input_file])
            else:
                self.update_status("Error: input_form.py not found")
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
    
    # debug, status function
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.after(3000, lambda: self.status_label.config(text="Ready"))

    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    app=MainMenu(root)
    app.run()


if __name__ == "__main__":
    main()
