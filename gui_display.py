import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import pickle as pkl
import os
from model import MUSHROOM_DATA_FILE, PARAMS_FILE, COLUMN_NAMES


class DataDisplayGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Mushroom Data & Parameters Viewer")
        self.root.geometry("1000x700")
        
        # Initialize data variables
        self.x = None
        self.y = None
        self.parameters = None
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create main notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.features_tab = ttk.Frame(self.notebook)
        self.target_tab = ttk.Frame(self.notebook)
        self.parameters_tab = ttk.Frame(self.notebook)
        self.summary_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.features_tab, text="Features (X)")
        self.notebook.add(self.target_tab, text="Target (y)")
        self.notebook.add(self.parameters_tab, text="Parameters")
        self.notebook.add(self.summary_tab, text="Summary")
        
        # Setup tabs
        self.setup_features_tab()
        self.setup_target_tab()
        self.setup_parameters_tab()
        self.setup_summary_tab()
        
        # Load data
        self.load_data()
    
    def create_menu_bar(self):
        """Create menu bar with File and Help menus"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Reload Data", command=self.load_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def setup_features_tab(self):
        """Setup the Features tab"""
        # Frame for info
        info_frame = ttk.LabelFrame(self.features_tab, text="Features Information", padding=10)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.features_info_text = tk.Text(info_frame, height=5, width=80)
        self.features_info_text.pack(fill=tk.X)
        
        # Frame for data
        data_frame = ttk.LabelFrame(self.features_tab, text="Features Data (First 10 rows)", padding=10)
        data_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview for features
        self.features_tree = ttk.Treeview(data_frame, height=15)
        self.features_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=self.features_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.features_tree.config(yscrollcommand=scrollbar.set)
    
    def setup_target_tab(self):
        """Setup the Target tab"""
        # Frame for info
        info_frame = ttk.LabelFrame(self.target_tab, text="Target Information", padding=10)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.target_info_text = tk.Text(info_frame, height=8, width=80)
        self.target_info_text.pack(fill=tk.X)
        
        # Frame for distribution
        dist_frame = ttk.LabelFrame(self.target_tab, text="Target Value Distribution", padding=10)
        dist_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.target_text = tk.Text(dist_frame, height=15)
        self.target_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_parameters_tab(self):
        """Setup the Parameters tab"""
        # Frame for info
        info_frame = ttk.LabelFrame(self.parameters_tab, text="Parameters Information", padding=10)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.params_info_text = tk.Text(info_frame, height=3, width=80)
        self.params_info_text.pack(fill=tk.X)
        
        # Frame for details
        details_frame = ttk.LabelFrame(self.parameters_tab, text="Parameter Details", padding=10)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.params_text = tk.Text(details_frame, height=20)
        self.params_text.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.params_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.params_text.config(yscrollcommand=scrollbar.set)
    
    def setup_summary_tab(self):
        """Setup the Summary tab"""
        self.summary_text = tk.Text(self.summary_tab, height=30)
        self.summary_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.summary_tab, orient=tk.VERTICAL, command=self.summary_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.summary_text.config(yscrollcommand=scrollbar.set)
    
    def load_data(self):
        try:
            
            df = pd.read_csv(
                MUSHROOM_DATA_FILE,
                header=None,
                names=COLUMN_NAMES,
                index_col=False
            )
            self.y = df['poisonous']
            self.x = df.drop('poisonous', axis=1)

            
            # Load parameters if they exist
            self.parameters = {}
            if os.path.exists(PARAMS_FILE):
                with open(PARAMS_FILE, "rb") as f:
                    self.parameters = pkl.load(f)
            
            # Update all tabs
            self.update_features_tab()
            self.update_target_tab()
            self.update_parameters_tab()
            self.update_summary_tab()
            
            messagebox.showinfo("Success", "Data loaded successfully!")
        
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"File not found: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def update_features_tab(self):
        if self.x is None:
            return
        
        # Clear previous data
        self.features_info_text.delete(1.0, tk.END)
        for item in self.features_tree.get_children():
            self.features_tree.delete(item)
        
        # Update info
        info = f"Shape: {self.x.shape}\n"
        info += f"Columns: {', '.join(self.x.columns)}\n"
        info += f"Data Types:\n{self.x.dtypes.to_string()}"
        
        self.features_info_text.insert(tk.END, info)
        self.features_info_text.config(state=tk.DISABLED)
        
        # Setup treeview columns
        self.features_tree['columns'] = list(self.x.columns)
        self.features_tree.column('#0', width=0, stretch=tk.NO)
        
        for col in self.x.columns:
            self.features_tree.column(col, anchor=tk.W, width=60)
            self.features_tree.heading(col, text=col, anchor=tk.W)
        
        # Insert data (first 10 rows)
        for idx, (_, row) in enumerate(self.x.head(10).iterrows()):
            values = [str(row[col]) for col in self.x.columns]
            self.features_tree.insert(parent='', index='end', iid=idx, text='', values=values)
    
    def update_target_tab(self):
        """Update the Target tab with data"""
        if self.y is None:
            return
        
        self.target_info_text.delete(1.0, tk.END)
        self.target_text.delete(1.0, tk.END)
        
        # Update info
        info = f"Shape: {self.y.shape}\n"
        info += f"Column name: {self.y.name}\n"
        info += f"Data type: {self.y.dtype}\n"
        info += f"Unique values: {self.y.nunique()}\n"
        
        self.target_info_text.insert(tk.END, info)
        self.target_info_text.config(state=tk.DISABLED)
        
        # Update distribution
        dist = "Value Counts:\n" + "=" * 40 + "\n"
        dist += self.y.value_counts().to_string()
        dist += "\n\n" + "=" * 40 + "\nFirst 20 values:\n"
        dist += self.y.head(20).to_string()
        
        self.target_text.insert(tk.END, dist)
        self.target_text.config(state=tk.DISABLED)
    
    def update_parameters_tab(self):
        """Update the Parameters tab with data"""
        self.params_info_text.delete(1.0, tk.END)
        self.params_text.delete(1.0, tk.END)
        
        if not self.parameters:
            self.params_info_text.insert(tk.END, "No parameters loaded (file not found)")
            self.params_info_text.config(state=tk.DISABLED)
            return
        
        # Update info
        info = f"Number of parameter groups: {len(self.parameters)} | Keys: {', '.join(self.parameters.keys())}"
        self.params_info_text.insert(tk.END, info)
        self.params_info_text.config(state=tk.DISABLED)
        
        # Update details
        details = "Parameter Details:\n" + "=" * 60 + "\n\n"
        for key, value in self.parameters.items():
            details += f"{key}:\n"
            details += f"  Type: {type(value).__name__}\n"
            
            if isinstance(value, (list, tuple)):
                details += f"  Length: {len(value)}\n"
                details += f"  Content: {str(value[:5])}{'...' if len(value) > 5 else ''}\n"
            elif isinstance(value, dict):
                details += f"  Keys: {list(value.keys())}\n"
            elif hasattr(value, 'shape'):
                details += f"  Shape: {value.shape}\n"
            else:
                details += f"  Value: {value}\n"
            
            details += "\n"
        
        self.params_text.insert(tk.END, details)
        self.params_text.config(state=tk.DISABLED)
    
    def update_summary_tab(self):
        """Update the Summary tab with statistical information"""
        self.summary_text.delete(1.0, tk.END)
        
        if self.x is None:
            return
        
        summary = "=" * 70 + "\n"
        summary += "MUSHROOM DATA SUMMARY\n"
        summary += "=" * 70 + "\n\n"
        
        summary += "📊 DATASET OVERVIEW\n"
        summary += "-" * 70 + "\n"
        summary += f"Total samples: {len(self.x)}\n"
        summary += f"Number of features: {len(self.x.columns)}\n"
        summary += f"Target classes: {self.y.nunique()}\n"
        summary += f"Data file: {MUSHROOM_DATA_FILE}\n\n"
        
        summary += "📈 FEATURES STATISTICS\n"
        summary += "-" * 70 + "\n"
        summary += self.x.describe().to_string()
        summary += "\n\n"
        
        summary += "🎯 TARGET DISTRIBUTION\n"
        summary += "-" * 70 + "\n"
        summary += self.y.value_counts().to_string()
        summary += "\n\n"
        
        if self.parameters:
            summary += "⚙️ LOADED PARAMETERS\n"
            summary += "-" * 70 + "\n"
            summary += f"Number of parameter groups: {len(self.parameters)}\n"
            summary += f"Keys: {', '.join(self.parameters.keys())}\n"
        else:
            summary += "⚙️ PARAMETERS\n"
            summary += "-" * 70 + "\n"
            summary += "No parameters file found\n"
        
        self.summary_text.insert(tk.END, summary)
        self.summary_text.config(state=tk.DISABLED)
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About",
            "Mushroom Data & Parameters Viewer\n\n"
            "A tkinter-based GUI application for viewing\n"
            "mushroom dataset and associated parameters.\n\n"
            "Version 1.0"
        )


def main():
    root = tk.Tk()
    app = DataDisplayGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
