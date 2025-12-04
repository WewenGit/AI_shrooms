import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from model import PROJECT_DIR, MUSHROOM_DATA_FILE


class DataInputGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Mushroom Data Input Form")
        self.root.geometry("600x800")
        
        self.column_names = ['cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor', 
                            'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color',
                            'stalk-shape', 'stalk-root', 'stalk-surface-above-ring',
                            'stalk-surface-below-ring', 'stalk-color-above-ring',
                            'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number',
                            'ring-type', 'spore-print-color', 'population', 'habitat']
        
        self.entry_widgets = {}
        self.input_data = {}
        
        # Load data to get unique values for each column
        self.load_unique_values()
        
        # Create main frame with scrollbar
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda _: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        title_label = ttk.Label(scrollable_frame, text="Mushroom Feature Input Form", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Create input fields for each column
        self.create_input_fields(scrollable_frame)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create button frame at bottom
        button_frame = ttk.Frame(root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.submit_button = ttk.Button(button_frame, text="Show Results", command=self.show_results)
        self.submit_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = ttk.Button(button_frame, text="Reset to Random", command=self.reset_to_random)
        self.reset_button.pack(side=tk.LEFT, padx=5)
    
    def load_unique_values(self):
        try:
            column_names = ['cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor', 
                           'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color',
                           'stalk-shape', 'stalk-root', 'stalk-surface-above-ring',
                           'stalk-surface-below-ring', 'stalk-color-above-ring',
                           'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number',
                           'ring-type', 'spore-print-color', 'population', 'habitat', 'class']
            
            df = pd.read_csv(MUSHROOM_DATA_FILE, header=None, names=column_names)
            
            # Store unique values for each column (excluding target)
            self.unique_values = {}
            for col in self.column_names:
                self.unique_values[col] = sorted(df[col].unique().tolist())
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
            self.unique_values = {col: [] for col in self.column_names}
    
    def create_input_fields(self, parent_frame):
        """Create input fields for each column"""
        for idx, col in enumerate(self.column_names):
            # Create frame for each row
            row_frame = ttk.Frame(parent_frame)
            row_frame.pack(fill=tk.X, pady=5, padx=5)
            
            # Label
            label = ttk.Label(row_frame, text=f"{col}:", width=25)
            label.pack(side=tk.LEFT, padx=5)
            
            # Combobox or Entry depending on number of unique values
            unique_vals = self.unique_values.get(col, [])
            
            if len(unique_vals) <= 20 and len(unique_vals) > 0:
                # Use Combobox for columns with few unique values
                widget = ttk.Combobox(row_frame, values=unique_vals, width=20, state="readonly")
                if unique_vals:
                    widget.current(0)  # Set default to first value
            else:
                # Use Entry for columns with many unique values
                widget = ttk.Entry(row_frame, width=25)
                if unique_vals:
                    widget.insert(0, unique_vals[0])  # Set default to first value
            
            widget.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            self.entry_widgets[col] = widget
    
    def get_input_data(self):
        """Get all input data from widgets"""
        data = {}
        for col, widget in self.entry_widgets.items():
            value = widget.get()
            if not value:
                messagebox.showwarning("Missing Value", f"Please provide a value for {col}")
                return None
            data[col] = value
        return data
    
    def show_results(self):
        """Show the combined results in a new window"""
        input_data = self.get_input_data()
        if input_data is None:
            return
        
        # Create new window for results
        result_window = tk.Toplevel(self.root)
        result_window.title("Input Results")
        result_window.geometry("600x400")
        
        # Create a frame with title
        title_frame = ttk.Frame(result_window)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(title_frame, text="Combined Input Data", 
                               font=("Arial", 12, "bold"))
        title_label.pack()
        
        # Create text widget to display results
        text_frame = ttk.Frame(result_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, height=20, width=70)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        # Display results in multiple formats
        results_text = "=" * 70 + "\n"
        results_text += "INPUT DATA - DICTIONARY FORMAT\n"
        results_text += "=" * 70 + "\n\n"
        results_text += "{\n"
        for col, value in input_data.items():
            results_text += f"  '{col}': '{value}',\n"
        results_text += "}\n\n"
        
        # Pandas Series format
        results_text += "=" * 70 + "\n"
        results_text += "INPUT DATA - PANDAS SERIES FORMAT\n"
        results_text += "=" * 70 + "\n\n"
        series = pd.Series(input_data)
        results_text += series.to_string()
        results_text += "\n\n"
        
        text_widget.insert(tk.END, results_text)
        text_widget.config(state=tk.DISABLED)
        
        # Create button frame for copy/export options
        button_frame = ttk.Frame(result_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        copy_button = ttk.Button(button_frame, text="Copy to Clipboard",
                                command=lambda: self.copy_to_clipboard(results_text))
        copy_button.pack(side=tk.LEFT, padx=5)
        
        save_button = ttk.Button(button_frame, text="Save to File",
                                command=lambda: self.save_to_file(input_data))
        save_button.pack(side=tk.LEFT, padx=5)
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Copied", "Results copied to clipboard!")
    
    def save_to_file(self, input_data):
        """Save input data to a CSV file"""
        try:
            df = pd.DataFrame([input_data])
            filepath = os.path.join(PROJECT_DIR, "input_data.csv")
            df.to_csv(filepath, index=False)
            messagebox.showinfo("Success", f"Data saved to {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
    
    def reset_to_random(self):
        """Reset all fields to random values from the dataset"""
        import random
        for col, widget in self.entry_widgets.items():
            unique_vals = self.unique_values.get(col, [])
            if unique_vals:
                random_value = random.choice(unique_vals)
                if isinstance(widget, ttk.Combobox):
                    widget.set(random_value)
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, random_value)
    
    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    app = DataInputGUI(root)
    app.run()


if __name__ == "__main__":
    main()
