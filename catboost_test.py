import tkinter as tk
from tkinter import ttk
import pandas as pd
from my_catboost.catboost_classifier import CatBoostAnalyzer as CBA

class DataInputGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("CatBoost Test")
        self.root.geometry("1000x800")
        
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
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        cba = CBA()
        cba.test()
        cba.prod()
        #input_data = self.get_test_data()
        #if input_data is None:
        #    return
        
        # Apply CatBoost
        #df = pd.DataFrame([input_data])
        #obs=self.rf.makeObservation(df)

        # Create new window for results
        result_window = tk.Toplevel(self.root)
        result_window.title("CatBoost Test")
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
        results_text += "CATBOOST - RESULT PREDICTION\n"
        results_text += "=" * 70 + "\n\n"
        results_text += "nothing yet"+"\n\n"
        results_text += "=" * 70 + "\n"
        results_text += "INPUT DATA - DICTIONARY FORMAT\n"
        results_text += "=" * 70 + "\n\n"
        results_text += "{\n"
        #for col, value in input_data.items():
            #results_text += f"  '{col}': '{value}',\n"
        results_text += "}\n\n"
        
        # Pandas Series format
        #results_text += "=" * 70 + "\n"
        #results_text += "INPUT DATA - PANDAS SERIES FORMAT\n"
        #results_text += "=" * 70 + "\n\n"
        #series = pd.Series(input_data)
        #results_text += series.to_string()
        #results_text += "\n\n"
        
        text_widget.insert(tk.END, results_text)
        text_widget.config(state=tk.DISABLED)
    
    
    
    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    app = DataInputGUI(root)
    app.run()


if __name__ == "__main__":
    main()
