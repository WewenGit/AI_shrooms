import os

# Define paths
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MUSHROOM_DATA_FILE = os.path.join(PROJECT_DIR, "mushroom", "agaricus-lepiota.data")
PARAMS_FILE = os.path.join(PROJECT_DIR, "parameters.pkl")

# to use only for debug
def display_loaded_data_info(x, y, parameters):
    print("=" * 60)
    print("LOADED DATA INFORMATION")
    print("=" * 60)
    
    # Features (X) information
    print("\n📊 FEATURES (X):")
    print(f"  Shape: {x.shape}")
    print(f"  Columns: {list(x.columns)}")
    print(f"  Data types:\n{x.dtypes}")
    print(f"\n  First few rows:\n{x.head()}")
    print(f"\n  Statistical summary:\n{x.describe()}")
    
    # Target (y) information
    print("\n" + "=" * 60)
    print("🎯 TARGET (y):")
    print(f"  Shape: {y.shape}")
    print(f"  Column name: {y.name}")
    print(f"  Data type: {y.dtype}")
    print(f"  Unique values: {y.nunique()}")
    print(f"  Value counts:\n{y.value_counts()}")
    print(f"\n  First few values:\n{y.head()}")
    
    # Parameters information
    if parameters:
        print("\n" + "=" * 60)
        print("⚙️ PARAMETERS:")
        print(f"  Number of parameter groups: {len(parameters)}")
        print(f"  Parameter keys: {list(parameters.keys())}")
        for key, value in parameters.items():
            print(f"\n  {key}:")
            if isinstance(value, (list, tuple)):
                print(f"    Type: {type(value).__name__}")
                print(f"    Length: {len(value)}")
                print(f"    Content: {value[:5]}..." if len(value) > 5 else f"    Content: {value}")
            elif isinstance(value, dict):
                print(f"    Type: dict")
                print(f"    Keys: {list(value.keys())}")
            elif hasattr(value, 'shape'):
                print(f"    Type: {type(value).__name__}")
                print(f"    Shape: {value.shape}")
            else:
                print(f"    Type: {type(value).__name__}")
                print(f"    Value: {value}")
    
    print("\n" + "=" * 60)