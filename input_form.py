import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import os
from model import PROJECT_DIR, COLUMN_NAMES, POSSIBLE_VALUES, MEANINGS
from random_forest.random_forest import RandomForestAnalyzer as RFA
from utils import importance_to_color


class DataInputGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Mushroom Data Input Form")
        self.root.geometry("1000x800")
        
        #random forest object
        self.rf = RFA()
        
        self.entry_widgets = {}
        self.input_data = {}
        
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
        
        # self.reset_button = ttk.Button(button_frame, text="Reset to Random", command=self.reset_to_random)
        # self.reset_button.pack(side=tk.LEFT, padx=5)
    
    def create_input_fields(self, parent_frame):

        importances=self.rf.compute_importance_feature()
        for feature, importance in importances.items():
            print(feature, importance)

        sorted_cols = [col for col in importances.index if col in COLUMN_NAMES[1:]]
        col_to_values = {col: POSSIBLE_VALUES[i] for i, col in enumerate(COLUMN_NAMES)}
        col_to_meanings = {col: MEANINGS[i] for i, col in enumerate(COLUMN_NAMES)}
        max_importance = np.max(importances)
        col_to_color = {col: importance_to_color(imp, max_val=max_importance) for col, imp in importances.items()}


        for col in sorted_cols:
            # Create frame for each row
            row_frame = ttk.Frame(parent_frame)
            row_frame.pack(fill=tk.X, pady=5, padx=5)
            
            # Color
            color = col_to_color[col]
            style = ttk.Style()
            style_name = f"{col}.TLabel"  # style unique par colonne
            style.configure(style_name, foreground=color)
            # Label
            label = ttk.Label(row_frame, text=f"{col}:", width=25, style=style_name)
            
            # Combobox or Entry depending on number of unique values
            unique_vals = col_to_values[col]
            
            if len(unique_vals) <= 20 and len(unique_vals) > 0:
                # Use Combobox for columns with few unique values
                widget = ttk.Combobox(row_frame, values=unique_vals, width=20, state="readonly")
                widget.config(state='normal')
                if unique_vals:
                    widget.current(0)  # Set default to first value
            else:
                # Use Entry for columns with many unique values
                widget = ttk.Entry(row_frame, width=25)
                widget.config(state='normal')
                if unique_vals:
                    widget.insert(0, unique_vals[0])  # Set default to first value

            # meanings
            label2 = ttk.Label(row_frame, text=col_to_meanings[col], width='auto')
            
            # Toggle button to enable/disable field
            # toggle_var = tk.BooleanVar(value=True)
            # toggle_btn = ttk.Checkbutton(row_frame, variable=toggle_var, w=widget, v=self.toggle_widget(widget))
            
            # toggle_btn.pack(side=tk.LEFT, padx=5)
            label.pack(side=tk.LEFT, padx=5)
            widget.pack(side=tk.LEFT, padx=5, fill=tk.X)
            label2.pack(side=tk.LEFT, padx=5)

            self.entry_widgets[col] = widget

    def get_input_data(self):
        data = {}
        for col, widget in self.entry_widgets.items():
            value = widget.get()
            if not value:
                messagebox.showwarning("Missing Value", f"Please provide a value for {col}")
                return None
            if str(widget['state'])=='normal':
                data[col] = value
        ordered_data = {key: data[key] for key in COLUMN_NAMES[1:]}
        return ordered_data
    
    def show_results(self):
        input_data = self.get_input_data()
        if input_data is None:
            return
        
        # Apply random forest
        df = pd.DataFrame([input_data])
        obs=self.rf.makeObservation(df)

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
        results_text += "RANDOM FOREST - RESULT PREDICTION\n"
        results_text += "=" * 70 + "\n\n"
        results_text += obs+"\n\n"
        results_text += "=" * 70 + "\n"
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
    
    #not used
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

    #not used
    def toggle_widget(self, widget):
        if widget['state'] == 'normal':
            widget.config(state='disabled')
        else:
            widget.config(state='normal')


def main():
    root = tk.Tk()
    app = DataInputGUI(root)
    app.run()


if __name__ == "__main__":
    main()
